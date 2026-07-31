# ----------------------------------------------------------------------
# Pull repo
# ----------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
import logging
import os
import shutil

# Third-party modules
from concurrent.futures import ThreadPoolExecutor

from pip._internal.index.collector import Link
from pip._internal.network.download import Downloader
from pip._internal.network.session import PipSession
from pip._internal.operations.prepare import unpack_url
from pip._internal.vcs.versioncontrol import VersionControl

from ..contrib.utils import check_destination, unpack
from ..models.db import db
from ..models.environment import Environment
from ..models.pulllog import PullLog
from ..models.role import Role

# Tower modules
from .base import API, api

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

VersionControl.check_destination = check_destination
VersionControl.unpack = unpack


class PullAPI(API):
    name = "pull"
    executor = ThreadPoolExecutor(2)

    @api
    def is_pulled(self, env_id):
        """Check repo is pulled and ready to deploy

        Args:
            env_id
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
            return {"success": False}
        with db.atomic():
            job = PullLog(
                start_ts=datetime.datetime.now(),
                environment=env,
                user=self.handler.current_user.name,
                repo=env.playbook_link,
            )
            job.save()
            self.executor.submit(self.pull_job_via_pip, job)
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

    def pull_job_via_pip(self, job):
        env = job.environment
        status = True
        log = []
        self.pull(env.playbook_link, env.repo_path)
        repo_playbooks_path = os.path.join(env.repo_path, "ansible")
        if not os.path.isdir(repo_playbooks_path):
            # Playbooks on repo root
            repo_playbooks_path = env.repo_path
        shutil.rmtree(env.playbook_path, ignore_errors=True)
        shutil.move(repo_playbooks_path, env.playbook_path)
        for role in Role.select().where(
            Role.environment == env, Role.is_enabled == True
        ):
            self.pull(role.link, role.role_path)

        with db.atomic():
            job.complete_ts = datetime.datetime.now()
            job.status = status
            job.log = "\n".join(log)
            job.save()

    @staticmethod
    def pull(link, path):
        logger.debug("Pull link: %s, path: %s", link, path)
        try:
            unpack_url(Link(link), path, Downloader(PipSession(), ""), 0)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.error("Pull error: %s", e)
