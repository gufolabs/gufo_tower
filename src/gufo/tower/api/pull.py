# ----------------------------------------------------------------------
# Pull repo
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
import logging
from concurrent.futures import ThreadPoolExecutor

# Third-party modules
from gufo.err import err

# Gufo Tower modules
from ..core.pull import prepare_env
from ..models.db import db
from ..models.environment import Environment
from ..models.pulllog import PullLog
from .base import API, api

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class PullAPI(API):
    name = "pull"
    executor = ThreadPoolExecutor(2)

    @api
    def is_pulled(self, env_id):
        """Check repo is pulled and ready to deploy.

        Args:
            env_id
        """
        try:
            env = Environment.get(Environment.id == int(env_id))
        except Environment.DoesNotExist:
            return False
        return (env.playbook_path / "site.yml").is_file()

    @api
    def start_job(self, env_id):
        try:
            env = Environment.get(Environment.id == int(env_id))
        except Environment.DoesNotExist:
            return {"success": False}
        with db.atomic():
            job = PullLog(
                start_ts=datetime.datetime.now(),
                environment=env,
                user=self.handler.current_user.name,
                repo=env.playbook_link,
            )
            job.save()
            self.executor.submit(self.pull_job, job)
            return {"success": True, "job": job.id}

    @api
    def get_job_status(self, env_id, job_id):
        with db.atomic():
            try:
                env = Environment.get(Environment.id == int(env_id))
            except Environment.DoesNotExist:
                return {"success": False}
            try:
                job = PullLog.get(
                    PullLog.id == int(job_id), PullLog.environment == env
                )
            except PullLog.DoesNotExist:
                return {"success": False}
        r = {
            "success": True,
            "complete": job.complete_ts is not None,
        }
        if r["complete"]:
            r["status"] = job.status
        return r

    def pull_job(self, job: PullLog) -> None:
        env = job.environment
        status = True
        log = "success"
        try:
            prepare_env(env)
        except BaseException as e:
            logger.error("Failed to pull: %s", e)
            err.process()
            status = False
            log = f"Failed: {e}"
        with db.atomic():
            job.complete_ts = datetime.datetime.now()
            job.status = status
            job.log = log
            job.save()
