# ----------------------------------------------------------------------
# Run ansible playbook
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import BinaryIO

# Third-party modules
import tornado.iostream
import tornado.process
import tornado.web

# Gufo Tower modules
from ..core.ansible import get_bin_path, to_ansible_environment
from ..models.db import db
from ..models.environment import Environment
from ..models.joblog import JobLog
from .base import BaseHandler

logger = logging.getLogger(__name__)


class DeployHandler(BaseHandler):
    SUPPORTED_METHODS = ("GET",)
    BUFFSIZE = 10485760

    rx_recap = re.compile(
        r"^(\S+)\s*:\s+"
        r"ok=(\d+)\s+changed=(\d+)\s+"
        r"unreachable=(\d+)\s+failed=(\d+)",
        re.MULTILINE,
    )

    def initialize(self):
        self.recap: dict[
            str, tuple[int, int, int, int]
        ] = {}  # node -> (ok, changed, unreachable, failed)
        self._env: Environment | None = None
        self._job_log: JobLog | None = None
        self._log_file: BinaryIO | None = None
        self.tags = ""
        self.ansible_verbose = ""
        self.connection_closed = False

    @property
    def environment(self) -> Environment:
        """Return current environment."""
        if self._env is None:
            msg = "Environment is not set"
            raise RuntimeError(msg)
        return self._env

    @property
    def job_log(self) -> JobLog:
        """Return current job log."""
        if self._job_log is None:
            msg = "JobLog is not set"
            raise RuntimeError(msg)
        return self._job_log

    @property
    def log_file(self) -> BinaryIO:
        """Return the open job log file."""
        if self._log_file is None:
            path = self.job_log.log_path
            path.parent.mkdir(parents=True, exist_ok=True)
            self._log_file = path.open("wb")
        return self._log_file

    @tornado.web.authenticated
    async def get(self, env_id: int, *args, **kwargs):
        """Run deploy."""
        try:
            self._env = Environment.get(Environment.id == env_id)
        except Environment.DoesNotExist as e:
            raise tornado.web.HTTPError(404) from e
        try:
            self.deploy_options = {
                int(i)
                for i in self.get_argument("deployment_options").split(",")
            }
        except BaseException as e:
            raise tornado.web.HTTPError(404) from e
        env = os.environ.copy()
        if self.get_argument("deployment_options"):
            tags = []
            if 1 in self.deploy_options:
                self.deploy_options -= set(range(90))
            if 10 in self.deploy_options:
                tags.append("get_source")
            if 50 in self.deploy_options and 51 not in self.deploy_options:
                tags.append("restart")
            if 51 in self.deploy_options:
                tags.append("soft_restart")
            if 90 in self.deploy_options:
                self.ansible_verbose = "-v"
            if 91 in self.deploy_options:
                self.ansible_verbose = "-vvvvvvvv"
            if 92 in self.deploy_options:
                env.update({"TOWER_SHOW_SECRETS": "1"})
            if 93 in self.deploy_options:
                env.update({"TOWER_RUN_CHECKS": "1"})
            if 94 in self.deploy_options:
                env.update({"TOWER_RUN_TESTS": "1"})
            if tags:
                self.tags = "--tags=" + ",".join(tags)
        logger.info(
            "Running deploy on %s %s", self._env.name, self.deploy_options
        )
        with db.atomic():
            self._job_log = JobLog(
                environment=self._env,
                start_ts=datetime.datetime.now(),
                user=self.current_user.name,
                playbook="site.yml",
            )
            self._job_log.save()
        # Disable nginx proxy buffering
        self.set_header("X-Accel-Buffering", "no")
        # Stream output
        self.write(f"Starting job #{self._job_log.id}\n\n")
        # Run playbook
        bin_path = get_bin_path()
        env.update(to_ansible_environment(self._env))
        command = [
            str(bin_path / "ansible-playbook"),
            "-i",
            str(bin_path / "tower-inv"),
            "site.yml",
            "-f 50",
            "--diff",
        ]
        if self.ansible_verbose:
            command.append(self.ansible_verbose)
        if self.tags:
            command.append(self.tags)
        logger.info("Running command %s", command)
        self.sp = tornado.process.Subprocess(
            command,
            env=env,
            stdout=tornado.process.Subprocess.STREAM,
            stderr=subprocess.STDOUT,
            cwd=str(self._env.playbook_path),
            close_fds=True,
        )
        self.write_pb()
        while True:
            try:
                data = await self.sp.stdout.read_bytes(
                    self.BUFFSIZE,
                    partial=True,
                )
            except tornado.iostream.StreamClosedError:
                break
            self.on_data(data)
        if not self.connection_closed:
            self.on_stream_close()

    def write_pb(self) -> None:
        """Generate the Ansible playbook from the service execution order."""
        from gufo.tower.models.service import Service

        order = Service.get_execution_order(self.environment)
        pb_order: list[Path] = []
        for service in order:
            pb = self.resolv_pb(service)
            if not pb:
                continue
            pb_order.append(pb)
        tower_autogen = self.environment.playbook_path / "tower.yml"
        tower_autogen.write_text(
            "".join(f"- import_playbook: {line}\n" for line in pb_order)
        )

    def resolv_pb(self, service: str) -> Path | None:
        """Resolve the playbook path for a service."""
        path = self.environment.roles_dir / service / "service.yml"
        if path.exists():
            return path
        path = (
            self.environment.playbook_path
            / "system_roles"
            / service
            / "service.yml"
        )
        if path.exists():
            return path
        path = (
            self.environment.playbook_path
            / "noc_roles"
            / service
            / "service.yml"
        )
        if path.exists():
            return path
        return None

    def on_connection_close(self, *args, **kwargs):
        """Handle client disconnection and terminate the running job."""
        logger.info("Connection terminated")
        self.connection_closed = True
        self.sp.stdout.close()
        super().on_connection_close(*args, **kwargs)
        self.log_file.write(b"\nConnection terminated\n")
        with db.atomic():
            self.job_log.complete_ts = datetime.datetime.now()
            self.job_log.save()

    def on_data(self, data: bytes) -> None:
        """Process and stream a chunk of Ansible output."""
        logger.debug(
            "PROGRESS: %s", data.removesuffix(b"\n").decode(errors="ignore")
        )
        self.write(data)
        self.flush()
        self.log_file.write(data)
        for match in self.rx_recap.finditer(data.decode()):
            g = match.groups()
            self.recap[g[0]] = tuple(int(x) for x in g[1:])

    def on_stream_close(self):
        """Finalize the deployment job and close the response."""
        logger.info("Deploy complete")
        self.close_log()
        self.finish()
        recap = (0, 0, 0, 0)
        for v in list(self.recap.values()):
            recap = tuple((x + y) for x, y in zip(recap, v, strict=True))
        with db.atomic():
            self.job_log.complete_ts = datetime.datetime.now()
            self.job_log.is_complete = True
            (
                self.job_log.n_ok,
                self.job_log.n_changed,
                self.job_log.n_unreachable,
                self.job_log.n_failed,
            ) = recap
            self.job_log.save()

    def close_log(self) -> None:
        """Close the job log file."""
        if self._log_file:
            self._log_file.close()
            self._log_file = None
