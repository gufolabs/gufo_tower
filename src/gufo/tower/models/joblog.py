# ----------------------------------------------------------------------
# JobLog model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from pathlib import Path

# Third-party modules
from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

# Tower modules
from ..config import config
from .db import db
from .environment import Environment


class JobLog(Model):
    """Store execution metadata and log for a playbook run."""

    class Meta:
        database = db
        table_name = "joblog"

    start_ts = DateTimeField()
    complete_ts = DateTimeField(null=True)
    environment = ForeignKeyField(Environment)
    user = CharField()
    playbook = CharField()
    log = TextField(default="")
    is_complete = BooleanField(default=False)
    n_ok = IntegerField(default=0)
    n_changed = IntegerField(default=0)
    n_unreachable = IntegerField(default=0)
    n_failed = IntegerField(default=0)

    @property
    def log_path(self) -> Path:
        """Return the path to the job log file.

        Returns:
            Path to the log file.
        """
        return config.log_dir / "jobs" / f"{self.id}.log"

    def append_log(self, data: bytes) -> None:
        """Append log data to the job log file.

        Args:
            data: Log data to append.
        """
        with open(self.log_path, "a") as fp:
            fp.write(data.decode())

    def get_log(self) -> str:
        """Return the job log contents.

        Returns:
            Job log contents, or an empty string if the log file does not
            exist.
        """
        if self.log_path.exists():
            return self.log_path.read_text()
        return ""
