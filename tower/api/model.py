# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Service API handler
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Third-party modules
import peewee
# Tower modules
from tower.models.db import db
from base import API, api, APIError


class ModelAPI(API):
    model = None  # ORM Model

    @api
    def get_items(self, cfg=None):
        """
        Returns list of items
        cfg may contain:
            limit
            page
            start
            filter
        :param cfg:
        :return:
        """
        cfg = cfg or {}
        limit = int(cfg.get("limit", 0))
        page = int(cfg.get("page", 0))
        filters = []
        for fd in cfg.get("filter", []):
            prop = fd.get("property")
            value = fd.get("value")
            if prop is None or value is None:
                continue
            field = getattr(self.model, prop, None)
            if not field:
                continue
            filters += [
                field == value
            ]
        with db.atomic():
            q = self.model.select()
            if filters:
                q = q.where(*filters)
            if limit:
                q = q.paginate(page, limit)
            data = [o.list_item() for o in q]
        return {
            "pos": 0,
            "total_count": len(data),
            "data": data
        }

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
            except peewee.DoesNotExist:
                raise APIError("Does not exists")
            for f in cfg:
                if f == "id":
                    continue
                setattr(record, f, cfg[f])
            record.save()
        return record.list_item()

    @api
    def delete_item(self, cfg):
        with db.atomic():
            try:
                record = self.model.get(self.model.id == int(cfg["id"]))
            except peewee.DoesNotExist:
                raise APIError("Does not exists")
            record.delete_instance()
        return True