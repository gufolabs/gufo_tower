# ----------------------------------------------------------------------
# Service API handler
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import peewee

# Tower modules
from ..models.db import db
from .base import API, APIError, api


class ModelAPI(API):
    model = None  # ORM Model

    DYNAMIC_FIRST_BATCH_SIZE = 30

    def render_items(self, cfg, format):
        """Render items.

        Returns list of items
        cfg may contain:
            start
            count
            filter
            sort - list of {name: ..., dir: <asc|desc>}

        Args:
            cfg
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
                msg = "Does not exists"
                raise APIError(msg) from e
        return record.list_item()

    @api
    def lookup_items(self, cfg):
        cfg = cfg or {}
        return self.render_items(cfg, lambda x: x.reference_item())

    @api
    def create_item(self, cfg):
        if "id" in cfg:
            del cfg["id"]
        record = self.model(**cfg)
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
            for f in cfg:
                if f in ("id", "environment"):
                    continue
                if getattr(record, f) != cfg[f]:
                    setattr(record, f, cfg[f])
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
