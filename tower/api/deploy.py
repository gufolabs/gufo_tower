# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Run ansible playbook
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python modules
import logging
import subprocess
import os
import re
import datetime
# Third-party modules
import tornado.web
import tornado.ioloop
import tornado.iostream
import tornado.process
# Tower modules
from base import BaseHandler
from tower.models.db import db
from tower.models.environment import Environment
from tower.models.joblog import JobLog

logger = logging.getLogger(__name__)


class DeployHandler(BaseHandler):
    SUPPORTED_METHODS = ("GET",)
    BUFFSIZE = 65536

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

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self, env_name, *args, **kwargs):
        try:
            self.env = Environment.get(Environment.name == env_name)
        except Environment.DoesNotExist:
            raise tornado.web.HTTPError(404)
        playbook = os.path.join(self.env.playbook_path, "ansible", "site.yml")
        logger.info("Running deploy on %s", self.env.name)
        with db.atomic():
            self.job_log = JobLog(
                environment=self.env,
                start_ts=datetime.datetime.now(),
                user=self.current_user.name,
                playbook="site.yml"
            )
            self.job_log.save()
        self.write("Starting job #%d\n\n" % self.job_log.id)
        self.sp = tornado.process.Subprocess(
            [
                "./bin/ansible-playbook",
                "-i", "./bin/tower-inv",
                playbook
            ],
            env={
                "NOC_ENV": str(self.env.name)
            },
            stdout=tornado.process.Subprocess.STREAM,
            stderr=subprocess.STDOUT
        )
        self.sp.stdout.set_close_callback(self.on_stream_close)
        self.read_future = self.sp.stdout.read_bytes(
            self.BUFFSIZE,
            streaming_callback=self.on_data,
            partial=True
        )

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
        logger.debug("DATA: '%s'", data)
        self.write(data)
        self.flush()
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
