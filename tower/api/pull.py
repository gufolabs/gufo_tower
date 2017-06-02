# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Pull repo
##----------------------------------------------------------------------
## Copyright (C) 2007-2016 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python modules
import logging
import subprocess
import datetime
import os
import shutil
import urlparse
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
        def update_hgrc(hgrc, url):
            p = urlparse.urlsplit(url)
            r = []
            if p.scheme in ("http", "https"):
                if "@" in p.netloc:
                    if p.username and p.password:
                        url = "%s://%s%s" % (p.scheme, p.netloc.rsplit("@")[-1], p.path)
                        r += ["[auth]"]
                        r += ["bb.prefix = %s" % url]
                        r += ["bb.username = %s" % p.username]
                        r += ["bb.password = %s" % p.password]
            r += ["[paths]"]
            r += ["default = %s" % url]
            r += ["[ui]"]
            logger.info("Updating %s", hgrc)
            with open(hgrc, "w") as f:
                f.write("\n".join(r))

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
                        "-b", env.branch,
                        "-r", env.changeset,
                        "-U",
                        env.repo,
                        env.repo_path
                    ]
                )
            #
            update_hgrc(os.path.join(env.repo_path, ".hg", "hgrc"), env.repo)
            # Pull updates
            logger.info("Updating %s", env.repo_path)
            subprocess.check_call(
                [
                    "./bin/hg",
                    "-q",
                    "--cwd=%s" % env.repo_path,
                    "pull",
                    "-b", env.branch,
                    "-r", env.changeset
                ]
            )
            #making noc.bz2
            logger.info("Archiving %s", env.repo_path)
            subprocess.check_call(
                [
                    "./bin/hg",
                    "-q",
                    "--cwd=%s" % env.repo_path,
                    "archive",
                    "-p", "noc",
                    "-t", "tbz2",
                    "%s/src_dist/noc.bz2" % env.data_path,
                    "-b", env.branch,
                    "-r", env.changeset
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
            if env.custom_repo:
                logger.info("Pulling custom repo")
                # Pull Repo
                if not os.path.exists(env.custom_repo_path):
                    logger.info("Cloning %s to %s",
                                env.custom_repo, env.custom_repo_path)
                    # Clone directory
                    subprocess.check_call(
                        [
                            "./bin/hg",
                            "-q",
                            "clone",
                            "-b", env.custom_branch,
                            "-r", env.custom_changeset,
                            "-U",
                            env.custom_repo,
                            env.custom_repo_path
                        ]
                    )
                #
                update_hgrc(os.path.join(env.custom_repo_path, ".hg", "hgrc"), env.custom_repo)
                # Pull updates
                logger.info("Updating %s", env.custom_repo_path)
                subprocess.check_call(
                    [
                        "./bin/hg",
                        "-q",
                        "--cwd=%s" % env.custom_repo_path,
                        "pull",
                        "-b", env.custom_branch,
                        "-r", env.custom_changeset
                    ]
                )
                #making custom.bz2
                logger.info("Archiving %s", env.custom_repo_path)
                subprocess.check_call(
                    [
                        "./bin/hg",
                        "-q",
                        "--cwd=%s" % env.custom_repo_path,
                        "archive",
                        "-p", "noc",
                        "-t", "tbz2",
                        "%s/src_dist/custom.bz2" % env.data_path,
                        "-r", env.changeset
                    ]
                )
            logger.info("Pulling complete")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.error("Pull error: %s", e)
            status = False
        with db.atomic():
            job.complete_ts = datetime.datetime.now()
            job.status = status
            job.log = "\n".join(log)
            job.save()
