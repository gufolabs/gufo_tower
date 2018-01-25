# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Pull repo
# ----------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

from __future__ import absolute_import

import datetime
# Python modules
import logging
import os

# Third-party modules
from concurrent.futures import ThreadPoolExecutor
from pip.download import unpack_url
from pip.index import Link
from pip.vcs import VersionControl

from tower.models.db import db
from tower.models.environment import Environment
from tower.models.pulllog import PullLog
# Tower modules
from .base import API, api
from tower.models.role import Role

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def unpack(self, location):
    """
    monkey patch pip library cause they always remove downloaded dir. no idea why
    """
    self.obtain(location)


VersionControl.unpack = unpack


class PullAPI(API):
    name = "pull"
    executor = ThreadPoolExecutor(2)

    @api
    def is_pulled(self, env_id):
        """
        Check repo is pulled and ready to deploy
        :param env_id:
        :return:
        """
        try:
            env = Environment.get(Environment.id == int(env_id))
        except Environment.DoesNotExist:
            return False
        playbook = os.path.join(env.playbook_path, "site.yml")
        return os.path.exists(playbook)

    @api
    def start_job(self, env_id):
        try:
            env = Environment.get(Environment.id == int(env_id))
        except Environment.DoesNotExist:
            return {
                "success": False
            }
        with db.atomic():
            job = PullLog(
                start_ts=datetime.datetime.now(),
                environment=env,
                user=self.handler.current_user.name,
                repo=env.playbook_link
            )
            job.save()
            self.executor.submit(self.pull_job_via_pip, job)
            return {
                "success": True,
                "job": job.id
            }

    @api
    def get_job_status(self, env_id, job_id):
        with db.atomic():
            try:
                env = Environment.get(Environment.id == int(env_id))
            except Environment.DoesNotExist:
                return {
                    "success": False
                }
            try:
                job = PullLog.get(PullLog.id == int(job_id),
                                  PullLog.environment == env)
            except PullLog.DoesNotExist:
                return {
                    "success": False
                }
        r = {
            "success": True,
            "complete": job.complete_ts is not None,
        }
        if r["complete"]:
            r["status"] = job.status
        return r

    def pull_job_via_pip(self, job):
        env = job.environment
        status = True
        log = []
        try:
            unpack_url(Link(env.playbook_link), env.playbook_path)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.error("Pull error: %s", e)
            status = False
        try:
            for role in Role.select().where(Role.environment == env, Role.is_enabled == True):
                unpack_url(Link(role.link), role.role_path)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.error("Roles pull error: %s", e)
            status = False

        with db.atomic():
            job.complete_ts = datetime.datetime.now()
            job.status = status
            job.log = "\n".join(log)
            job.save()
