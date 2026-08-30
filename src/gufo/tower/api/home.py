# ----------------------------------------------------------------------
# Home API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
from dataclasses import dataclass
from typing import ClassVar, TypedDict

# Third-party modules
import peewee

# Gufo Tower modules
from .. import __version__
from ..config import config
from ..models.datacenter import Datacenter
from ..models.environment import Environment
from ..models.joblog import JobLog
from ..models.node import Node
from ..models.pool import Pool
from ..utils import get_size, humanize_duration, humanize_size
from .base import API, api


class DeployData(TypedDict):
    """Deployment status data for the environments table."""

    ts: str
    status: bool
    duration: str


@dataclass
class DeployStatus:
    """Store the status and timing information of the last deployment.

    Attributes:
        ts: Completion timestamp of the deployment.
        status: True if the deployment completed without failures.
        duration: Deployment duration in seconds.
    """

    ts: datetime.datetime
    status: bool
    duration: float

    def to_data(self) -> DeployData:
        """Return deployment status as template data."""
        return {
            "ts": self.ts.strftime("%Y-%m-%d %H:%M"),
            "status": self.status,
            "duration": humanize_duration(self.duration),
        }


class EnvironmentData(TypedDict):
    """Environment data for the environments table."""

    id: int
    name: str
    web_host: str
    url: str
    env_type: str
    installation_name: str
    pools: int
    datacenters: int
    nodes: int
    tag: str
    total_vcpu: int | None
    total_memory_mb: int | None
    deploy_status: DeployData | None


class HomeData(TypedDict):
    """Template data for the home page."""

    version: str
    db_size: str
    home_size: str
    github: str
    environments: list[EnvironmentData]


class HomeAPI(API):
    name = "home"
    ENV_TYPES: ClassVar[dict[str, str]] = dict(Environment.env_type.choices)

    @api
    def get_data(self) -> HomeData:
        """Returns template data."""
        return {
            "version": __version__,
            "db_size": humanize_size(get_size(config.db_path)),
            "home_size": humanize_size(get_size(config.home)),
            "github": "https://github.com/gufolabs/gufo_tower/",
            "environments": self.get_environments(),
        }

    def get_environments(self) -> list[EnvironmentData]:
        """Get list of environments."""
        deploy_status = self.get_deploy_status()
        return [
            self.get_environment(env, deploy_status.get(env.id))
            for env in Environment.select()
        ]

    def get_environment(
        self, env: Environment, deploy_status: DeployStatus | None
    ) -> EnvironmentData:
        """Get row for environments table."""
        pools = Pool.select().where(Pool.environment == env).count()
        datacenters = (
            Datacenter.select()
            .join(Node)
            .where(Node.environment == env)
            .distinct()
            .count()
        )
        nodes = Node.select().where(Node.environment == env).count()
        total_vcpu = (
            Node.select(peewee.fn.COALESCE(peewee.fn.SUM(Node.vcpu), 0))
            .where(Node.environment == env)
            .scalar()
        )
        total_memory_mb = (
            Node.select(peewee.fn.COALESCE(peewee.fn.SUM(Node.memory_mb), 0))
            .where(Node.environment == env)
            .scalar()
        )
        _, _, tag = env.playbook_link.partition("@")
        return {
            "id": env.id,
            "name": env.name,
            "web_host": env.web_host,
            "url": f"https://{env.web_host}/",
            "env_type": self.ENV_TYPES[env.env_type],
            "installation_name": env.installation_name,
            "pools": pools,
            "datacenters": datacenters,
            "nodes": nodes,
            "tag": tag or "-",
            "total_vcpu": total_vcpu,
            "total_memory_mb": total_memory_mb,
            "deploy_status": deploy_status.to_data()
            if deploy_status
            else None,
        }

    def get_deploy_status(self) -> dict[int, DeployStatus]:
        """Return the status of the last completed deployment per environment.

        Returns:
            A mapping from environment ID to the status of its last completed
            deployment.
        """
        last_jobs = (
            JobLog.select(peewee.fn.MAX(JobLog.id).alias("id"))
            .where(JobLog.is_complete)
            .group_by(JobLog.environment)
        )

        jobs = JobLog.select(
            JobLog.environment,
            JobLog.start_ts,
            JobLog.complete_ts,
            JobLog.n_failed,
            JobLog.n_unreachable,
        ).where(JobLog.id.in_(last_jobs))

        return {
            job.environment_id: DeployStatus(
                ts=job.complete_ts,
                status=(job.n_failed + job.n_unreachable) == 0,
                duration=(job.complete_ts - job.start_ts).total_seconds(),
            )
            for job in jobs
        }
