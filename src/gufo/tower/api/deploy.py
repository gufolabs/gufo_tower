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
import sys
from pathlib import Path

# Third-party modules
import tornado.iostream
import tornado.process
import tornado.web

# Gufo Tower modules
from .. import __version__
from ..core.ssh import build_ssh_keys
from ..models.db import db
from ..models.environment import Environment
from ..models.joblog import JobLog
from ..models.pool import Pool
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
        self.play_log: list[bytes] = []
        self.env: Environment | None = None
        self.job_log: JobLog | None = None
        self.tags = ""
        self.ansible_verbose = ""
        self.connection_closed = False

    @property
    def environment(self) -> Environment:
        """Return current environment."""
        if self.env is None:
            msg = "Environment is not set"
            raise RuntimeError(msg)
        return self.env

    @property
    def joblog(self) -> JobLog:
        """Return current job log."""
        if self.job_log is None:
            msg = "JobLog is not set"
            raise RuntimeError(msg)
        return self.job_log

    @tornado.web.authenticated
    async def get(self, env_id: int, *args, **kwargs):
        try:
            self.env = Environment.get(Environment.id == env_id)
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
            "Running deploy on %s %s", self.env.name, self.deploy_options
        )
        with db.atomic():
            self.job_log = JobLog(
                environment=self.env,
                start_ts=datetime.datetime.now(),
                user=self.current_user.name,
                playbook="site.yml",
            )
            self.job_log.save()
        # Disable nginx proxy buffering
        self.set_header("X-Accel-Buffering", "no")
        # Stream output
        self.write(f"Starting job #{self.job_log.id}\n\n")
        # Generate ssh keys
        for pool in Pool.select().where(Pool.environment == self.env):
            build_ssh_keys(
                f"{pool.name}@noc", self.env.ssh_keys_path / pool.name
            )
        # Run playbook
        bin_path = Path(sys.argv[0]).resolve().parent
        if os.path.exists("/.dockerenv"):
            ansible_ssh_cp = os.path.join(
                "/root/.ansible/cp/ansible-ssh-%%r-%%h-%%r"
            )
        else:
            ansible_ssh_cp = os.path.join("/tmp/tower-%%r-%%h-%%r")
        env.update(
            {
                "NOC_ENV": str(self.env.name),
                "ANSIBLE_SSH_CONTROL_PATH": ansible_ssh_cp,
                "ANSIBLE_SSH_PIPELINING": "1",
                "ANSIBLE_REMOTE_TEMP": "/tmp/${USER}/ansible",
                "ANSIBLE_HOST_KEY_CHECKING": "False",
                "ANSIBLE_STDOUT_CALLBACK": "debug",
                "ANSIBLE_ROLES_PATH": ":".join(
                    [
                        str(self.env.roles_dir),
                        str(self.env.playbook_path / "system_roles"),
                        str(self.env.playbook_path / "noc_roles"),
                    ]
                ),
                "PYTHONUNBUFFERED": "1",
                "TOWER_VERSION": __version__,
            }
        )
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
            cwd=str(self.env.playbook_path),
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
        logger.info("Connection terminated")
        self.connection_closed = True
        self.sp.stdout.close()
        super().on_connection_close(*args, **kwargs)
        self.play_log.append(b"\nConnection terminated\n")
        with db.atomic():
            self.joblog.complete_ts = datetime.datetime.now()
            self.joblog.log = (b"".join(self.play_log)).decode()
            self.joblog.save()

    def on_data(self, data: bytes) -> None:
        def qlog(x):
            if x.endswith(b"\n"):
                return x[:-1]
            return x

        logger.debug("PROGRESS: %s", qlog(data))
        self.write(data)
        self.flush()
        self.joblog.append_log(data)
        for match in self.rx_recap.finditer(data.decode()):
            g = match.groups()
            self.recap[g[0]] = tuple(int(x) for x in g[1:])
        self.play_log.append(data)

    def on_stream_close(self):
        logger.info("Deploy complete")
        self.finish()
        recap = (0, 0, 0, 0)
        for v in list(self.recap.values()):
            recap = tuple((x + y) for x, y in zip(recap, v, strict=True))
        with db.atomic():
            self.joblog.complete_ts = datetime.datetime.now()
            self.joblog.is_complete = True
            self.joblog.log = "".join(str(self.play_log))
            (
                self.joblog.n_ok,
                self.joblog.n_changed,
                self.joblog.n_unreachable,
                self.joblog.n_failed,
            ) = recap
            self.joblog.save()
