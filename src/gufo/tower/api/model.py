# ----------------------------------------------------------------------
# Service API handler
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from collections.abc import Callable
from typing import Any, ClassVar, Literal, TypedDict

# Third-party modules
import peewee

# Tower modules
from ..models.db import db
from .base import API, APIError, api


class RenderSort(TypedDict):
    """Sort descriptor for rendered model items.

    Attributes:
        id: Model field name to sort by.
        dir: Sort direction, either ``"asc"`` or ``"desc"``.
    """

    id: str
    dir: Literal["asc", "desc"]


class RenderFilter(TypedDict):
    """Filter descriptor for rendered model items.

    Attributes:
        property: Model field name to filter by.
        value: Value to compare the field against.
    """

    property: str
    value: Any


class RenderConfig(TypedDict, total=False):
    """Configuration for rendering model items.

    Attributes:
        start: Number of items to skip.
        count: Maximum number of items to return.
        dynamic: Enable dynamic loading and return ``total_count``
            for the first batch.
        filter: List of filter descriptors.
        sort: A sort descriptor or a list of sort descriptors.
    """

    start: int | str
    count: int | str
    dynamic: bool
    filter: list[RenderFilter]
    sort: RenderSort | list[RenderSort]


class ModelAPI(API):
    model: ClassVar[type[peewee.Model]]

    DYNAMIC_FIRST_BATCH_SIZE = 30
    ignored_fields: ClassVar[set[str] | None] = None

    def render_items(
        self, cfg: RenderConfig, format: Callable[[Any], Any]
    ) -> dict[str, Any]:
        """Render a paginated and optionally filtered model query.

        The configuration supports pagination, filtering, sorting and
        dynamic loading.

        Args:
        cfg: Query configuration containing:
            start: Number of items to skip.
            count: Maximum number of items to return.
            dynamic: Enable dynamic loading and return ``total_count``
                for the first batch.
            filter: List of filters with ``property`` and ``value``.
            sort: A sort descriptor or a list of descriptors. Each
                descriptor contains ``id`` and optional ``dir``
                (``"asc"`` or ``"desc"``).
        format: Callable used to convert each model instance into the
            returned representation.

        Returns:
            A dictionary containing ``pos`` and ``data``. When dynamic
            loading is enabled for the first batch, it also contains
            ``total_count``.
        """
        dynamic = "dynamic" in cfg
        start = int(cfg.get("start", 0))
        count = int(cfg.get("count", 0))
        sort = cfg.get("sort", [])
        filters = []
        sorters = []
        total_count = None
        # Apply dynamic limits
        if dynamic and not count:
            count = self.DYNAMIC_FIRST_BATCH_SIZE
        # Process sorters
        if isinstance(sort, dict):
            sort = [sort]
        for s in sort:
            name = str(s.get("id"))
            direction = s.get("dir", "asc")
            if direction == "desc":
                sorters += [-getattr(self.model, name)]
            else:
                sorters += [getattr(self.model, name)]
        # Process filters
        for fd in cfg.get("filter", []):
            prop = fd.get("property")
            value = fd.get("value")
            if prop is None or value is None:
                continue
            field = getattr(self.model, prop, None)
            if not field:
                continue
            filters += [field == value]
        with db.atomic():
            q = self.model.select()
            if filters:
                q = q.where(*filters)
            if dynamic and not start:
                total_count = q.count()
            if start:
                q = q.offset(start)
            if count:
                q = q.limit(count)
            if sorters:
                q = q.order_by(*sorters)
            data = [format(o) for o in q]
        r = {"pos": start, "data": data}
        if dynamic and not start:
            r["total_count"] = total_count
        return r

    def clean(self, cfg: dict[str, Any]) -> dict[str, Any]:
        """Remove ignored fields from the configuration.

        Args:
            cfg: Configuration dictionary to clean.

        Returns:
            A configuration dictionary without fields listed in
            ``ignored_fields``. Returns the original dictionary if no fields
            are ignored.
        """
        to_ignore = {"id"}
        if self.ignored_fields:
            to_ignore |= self.ignored_fields
        return {k: v for k, v in cfg.items() if k not in to_ignore}

    @api
    def get_items(self, cfg=None):
        cfg = cfg or {}
        return self.render_items(cfg, lambda x: x.list_item())

    @api
    def get_item(self, cfg):
        with db.atomic():
            try:
                record = self.model.get(self.model.id == int(cfg["id"]))
            except peewee.DoesNotExist as e:
                msg = "Does not exist"
                raise APIError(msg) from e
        return record.list_item()

    @api
    def lookup_items(self, cfg):
        cfg = cfg or {}
        return self.render_items(cfg, lambda x: x.reference_item())

    @api
    def create_item(self, cfg):
        record = self.model(**self.clean(cfg))
        with db.atomic():
            record.save()
        return record.list_item()

    @api
    def update_item(self, cfg):
        with db.atomic():
            try:
                record = self.model.get(self.model.id == int(cfg["id"]))
            except peewee.DoesNotExist as e:
                msg = "Does not exists"
                raise APIError(msg) from e
            for k, v in self.clean(cfg).items():
                if k == "environment":
                    continue  # Cannot change environment
                if getattr(record, k) != v:
                    setattr(record, k, v)
            record.save()
        return record.list_item()

    @api
    def delete_item(self, cfg):
        with db.atomic():
            try:
                record = self.model.get(self.model.id == int(cfg["id"]))
            except peewee.DoesNotExist as e:
                msg = "Does not exists"
                raise APIError(msg) from e
            record.delete_instance()
        return True
