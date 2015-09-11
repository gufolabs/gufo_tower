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
# Third-party modules
import tornado.web
import tornado.ioloop
import tornado.iostream
import tornado.process
# Tower modules
from tower.models.environment import Environment

logger = logging.getLogger(__name__)


class DeployHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET",)
    BUFFSIZE = 65536

    def get(self, env_name, *args, **kwargs):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
        try:
            env = Environment.get(Environment.name == env_name)
        except Environment.DoesNotExist:
            raise tornado.web.HTTPError(404)
        logger.info("Running deploy on %s", env.name)
        self.sp = tornado.process.Subprocess(
            [
                "./bin/ansible-playbook",
                "-i", "./bin/inv",
                os.path.join(env.playbook_path, "ansible", "site.yml")
            ],
            env={
                "NOC_ENV": str(env.name)
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

    def on_data(self, data):
        logger.debug("DATA: %s", data)
        self.write(data)
        self.flush()

    def on_stream_close(self):
        logger.info("Deploy complete")
        self.finish()
        try:
            self.read_future.result()
        except tornado.iostream.StreamClosedError:
            pass
