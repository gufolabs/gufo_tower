# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Pull repo
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python modules
import logging
import subprocess
import datetime
import os
import shutil
# Third-party modules
from concurrent.futures import ThreadPoolExecutor
# Tower modules
from base import API, api
from tower.models.db import db
from tower.models.environment import Environment
from tower.models.pulllog import PullLog

logger = logging.getLogger(__name__)


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
        playbook = os.path.join(env.playbook_path, "ansible", "site.yml")
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
                repo=env.repo,
                branch=env.branch,
                changeset=env.changeset
            )
            job.save()
            self.executor.submit(self.pull_job, job)
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

    def pull_job(self, job):
        """
        Pull worker job
        :param env:
        :return:
        """
        env = job.environment
        status = True
        log = []
        try:
            # Pull Repo
            if not os.path.exists(env.repo_path):
                logger.info("Cloning %s to %s", env.repo, env.repo_path)
                # Clone directory
                subprocess.check_call(
                    [
                        "./bin/hg",
                        "-q",
                        "clone",
                        "-U",
                        env.repo,
                        env.repo_path
                    ]
                )
            # Pull updates
            logger.info("Updating %s", env.repo_path)
            subprocess.check_call(
                [
                    "./bin/hg",
                    "-q",
                    "--cwd=%s" % env.repo_path,
                    "pull"
                ]
            )
            # Fetch playbooks
            logger.info("Updating playbooks")
            shutil.rmtree(env.playbook_path, ignore_errors=True)
            if env.changeset == "tip":
                rev = env.branch
            else:
                rev = env.changeset
            subprocess.check_call(
                [
                    "./bin/hg",
                    "-q",
                    "--cwd=%s" % env.repo_path,
                    "archive",
                    "-r", rev,
                    "-I", "ansible/**",
                    os.path.join("..", "..", "..", "..", env.playbook_path)
                ]
            )
            logger.info("Pulling complete")
        except KeyboardInterrupt:
            raise
        except:
            logger.error("Pull error")
            status = False
        with db.atomic():
            job.complete_ts = datetime.datetime.now()
            job.status = status
            job.log = "\n".join(log)
            job.save()
