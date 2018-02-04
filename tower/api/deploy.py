# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Run ansible playbook
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

from __future__ import absolute_import
import datetime
# Python modules
import logging
import os
import re
import subprocess

import tornado.ioloop
import tornado.iostream
import tornado.process
# Third-party modules
import tornado.web

# Tower modules
from .base import BaseHandler
from tower.models.db import db
from tower.models.environment import Environment
from tower.models.joblog import JobLog
from tower.models.settings import Settings

logger = logging.getLogger(__name__)


class DeployHandler(BaseHandler):
    SUPPORTED_METHODS = ("GET",)
    BUFFSIZE = 10485760

    rx_recap = re.compile(
        r"^(\S+)\s*:\s+"
        r"ok=(\d+)\s+changed=(\d+)\s+"
        r"unreachable=(\d+)\s+failed=(\d+)\s*$",
        re.MULTILINE
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
    def get(self, env_name, *args, **kwargs):
        try:
            self.env = Environment.get(Environment.name == env_name)
        except Environment.DoesNotExist:
            raise tornado.web.HTTPError(404)
        try:
            self.deploy_options = set([int(i) for i in self.get_argument("deployment_options").split(",")])
        except:  # noqa
            raise tornado.web.HTTPError(404)
        if self.get_argument("deployment_options"):
            tags = []
            if 1 in self.deploy_options:
                self.deploy_options -= set(range(90))
            if 10 in self.deploy_options:
                tags.append("get_source")
            if 11 in self.deploy_options:
                tags.append("config")
            if 12 in self.deploy_options:
                tags.append("requirements")
            if 13 in self.deploy_options:
                tags.append("migrate")
            if 50 in self.deploy_options and 51 not in self.deploy_options:
                tags.append("restart")
            if 51 in self.deploy_options:
                tags.append("soft_restart")
            if 90 in self.deploy_options:
                self.ansible_verbose = "-v"
            if 91 in self.deploy_options:
                self.ansible_verbose = "-vvvvvvvv"
            if tags:
                self.tags = "--tags=" + ",".join(tags)
        logger.info("Running deploy on %s %s", self.env.name, self.deploy_options)
        with db.atomic():
            self.job_log = JobLog(
                environment=self.env,
                start_ts=datetime.datetime.now(),
                user=self.current_user.name,
                playbook="site.yml"
            )
            self.job_log.save()
        # Disable nginx proxy buffering
        self.set_header("X-Accel-Buffering", "no")
        # Stream output
        self.write("Starting job #%d\n\n" % self.job_log.id)
        self.get_version()
        # Generate ssh keys
        self.env.build_ssh_keys()
        # Run playbook
        bin_path = os.path.abspath(os.path.join(os.getcwd(), "bin"))
        if os.path.exists("/.dockerenv"):
            ansible_ssh_cp = os.path.join("/root/.ansible/cp/ansible-ssh-%%r-%%h-%%r")
        else:
            ansible_ssh_cp = os.path.join(
                "/tmp/tower-%%r-%%h-%%r"
            )
        env = os.environ.copy()
        env.update({
            "NOC_ENV": str(self.env.name),
            "ANSIBLE_SSH_CONTROL_PATH": ansible_ssh_cp,
            "ANSIBLE_SSH_PIPELINING": "1",
            "ANSIBLE_REMOTE_TEMP": "/tmp/${USER}/ansible",
            "ANSIBLE_HOST_KEY_CHECKING": "False",
            "ANSIBLE_STDOUT_CALLBACK": "debug",
            "ANSIBLE_ROLES_PATH": ":".join([
                self.env.roles_prefix,
                os.path.join(self.env.playbook_path, "system_roles"),
                os.path.join(self.env.playbook_path, "noc_roles")
            ]),
            "PYTHONUNBUFFERED": "1",
            "TOWER_VERSION": self.version
        })
        command = [
            os.path.join(bin_path, "ansible-playbook"),
            "-i", os.path.join(bin_path, "tower-inv"),
            "site.yml", "-f 50", "--diff"
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
            cwd=os.path.join(self.env.playbook_path),
            close_fds=True
        )
        self.write_pb()
        self.sp.stdout.set_close_callback(self.on_stream_close)
        self.read_future = self.sp.stdout.read_bytes(
            self.BUFFSIZE,
            streaming_callback=self.on_data,
            partial=True
        )

    def write_pb(self):
        from tower.models.service import Service
        order = Service.get_execution_order(self.env)
        pb_order = []
        for service in order:
            pb = self.resolv_pb(service)
            if not pb:
                continue
            pb_order.append(pb)
        tower_autogen = os.path.abspath(os.path.join(self.env.playbook_path, "tower.yml"))
        with open(tower_autogen, "w") as f:
            for line in pb_order:
                f.write("- import_playbook: %s\n" % line)

    def resolv_pb(self, service):
        if os.path.exists(
                os.path.join(self.env.roles_prefix, service, "service.yml")
        ):
            return os.path.join(
                self.env.roles_prefix, service, "service.yml"
            )
        elif os.path.exists(
                os.path.join(self.env.playbook_path, "system_roles", service, "service.yml")
        ):
            return os.path.join(
                self.env.playbook_path, "system_roles", service, "service.yml"
            )
        elif os.path.exists(
                os.path.join(self.env.playbook_path, "noc_roles", service, "service.yml")
        ):
            return os.path.join(
                self.env.playbook_path, "noc_roles", service, "service.yml"
            )
        else:
            return None

    def get_version(self):
        from os.path import realpath, join, dirname, abspath
        version_path = realpath(join(dirname(abspath(__file__)), '../../../../../VERSION'))
        if not os.path.exists(version_path):
            self.version = 'old'
        else:
            with open(version_path, "r") as f:
                self.version = f.read().splitlines()[0]

    def on_connection_close(self, *args, **kwargs):
        logger.info("Connection terminated")
        self.sp.stdout.close()
        super(DeployHandler, self).on_connection_close(*args, **kwargs)
        self.play_log += ["\nConnection terminated\n"]
        with db.atomic():
            self.job_log.complete_ts = datetime.datetime.now()
            self.job_log.log = "".join(self.play_log)
            self.job_log.save()

    def on_data(self, data):
        def qlog(x):
            if x.endswith("\n"):
                return x[:-1]
            else:
                return x

        logger.debug("PROGRESS: %s", qlog(data))
        self.write(data)
        self.flush()
        self.job_log.append_log(data)
        for match in self.rx_recap.finditer(data):
            g = match.groups()
            self.recap[g[0]] = [int(x) for x in g[1:]]
        self.play_log += [data]

    def on_stream_close(self):
        logger.info("Deploy complete")
        self.finish()
        try:
            self.read_future.result()
        except tornado.iostream.StreamClosedError:
            pass
        recap = [0, 0, 0, 0]
        for v in self.recap.itervalues():
            recap = [(x + y) for x, y in zip(recap, v)]
        with db.atomic():
            self.job_log.complete_ts = datetime.datetime.now()
            self.job_log.is_complete = True
            self.job_log.log = "".join(self.play_log)
            (self.job_log.n_ok, self.job_log.n_changed,
             self.job_log.n_unreachable, self.job_log.n_failed) = recap
            self.job_log.save()
