# ----------------------------------------------------------------------
# Run ansible playbook
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import contextlib
import datetime
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Optional

# Third-party modules
import tornado.iostream
import tornado.process
import tornado.web

# Gufo Tower modules
from .. import __version__
from ..config import config
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
        r"unreachable=(\d+)\s+failed=(\d+)\s*$",
        re.MULTILINE,
    )

    def initialize(self):
        self.recap = {}  # node -> (ok, changed, unreachable, failed)
        self.play_log = []
        self.env = None
        self.job_log = None
        self.tags = ""
        self.ansible_verbose = ""

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self, env_id, *args, **kwargs):
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
        self.env.build_ssh_keys()
        # Run playbook
        bin_path = Path.cwd() / "bin"
        if config.in_docker:
            ansible_ssh_cp = (
                Path("/root/.ansible/cp") / "ansible-ssh-%%r-%%h-%%r"
            )
        else:
            ansible_ssh_cp = Path("/tmp") / "tower-%%r-%%h-%%r"
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
            "-f",
            "50",
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
        self.sp.stdout.set_close_callback(self.on_stream_close)
        self.read_future = self.sp.stdout.read_bytes(
            self.BUFFSIZE, streaming_callback=self.on_data, partial=True
        )

    def write_pb(self):
        from gufo.tower.models.service import Service

        order = Service.get_execution_order(self.env)
        pb_order = []
        for service in order:
            pb = self.resolv_pb(service)
            if not pb:
                continue
            pb_order.append(pb)
        tower_autogen = (self.env.playbook_path / "tower.yml").resolve()
        with open(tower_autogen, "w") as f:
            for line in pb_order:
                f.write(f"- import_playbook: {line}\n")

    def resolv_pb(self, service) -> Optional[Path]:
        path = self.env.roles_dir / service / "service.yml"
        if path.exists():
            return path
        path = (
            self.env.playbook_path / "system_roles" / service / "service.yml"
        )
        if path.exists():
            return path
        path = self.env.playbook_path / "noc_roles" / service / "service.yml"
        if path.exists():
            return path
        return None

    def on_connection_close(self, *args, **kwargs):
        logger.info("Connection terminated")
        self.sp.stdout.close()
        super().on_connection_close(*args, **kwargs)
        self.play_log += ["\nConnection terminated\n"]
        with db.atomic():
            self.job_log.complete_ts = datetime.datetime.now()
            self.job_log.log = "".join(self.play_log)
            self.job_log.save()

    def on_data(self, data):
        def qlog(x):
            if x.endswith(b"\n"):
                return x[:-1]
            return x

        logger.debug("PROGRESS: %s", qlog(data))
        self.write(data)
        self.flush()
        self.job_log.append_log(data)
        for match in self.rx_recap.finditer(str(data)):
            g = match.groups()
            self.recap[g[0]] = [int(x) for x in g[1:]]
        self.play_log += [data]

    def on_stream_close(self):
        logger.info("Deploy complete")
        self.finish()
        with contextlib.suppress(tornado.iostream.StreamClosedError):
            self.read_future.result()
        recap = [0, 0, 0, 0]
        for v in list(self.recap.values()):
            recap = [(x + y) for x, y in zip(recap, v)]
        with db.atomic():
            self.job_log.complete_ts = datetime.datetime.now()
            self.job_log.is_complete = True
            self.job_log.log = "".join(str(self.play_log))
            (
                self.job_log.n_ok,
                self.job_log.n_changed,
                self.job_log.n_unreachable,
                self.job_log.n_failed,
            ) = recap
            self.job_log.save()
