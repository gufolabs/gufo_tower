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
from base import API, api


class ModelAPI(API):
    model = None  # ORM Model

    @api
    def read_items(self, cfg):
        limit = int(cfg.get("limit", 0))
        page = int(cfg.get("page", 0))
        with db.atomic():
            q = self.model.select()
            if limit:
                q = q.paginate(page, limit)
            data = [o.list_item() for o in q]
        return {
            "data": data,
            "total": len(data),
            "success": True
        }

    @api
    def create_item(self, cfg):
        if "id" in cfg:
            del cfg["id"]
        record = self.model(**cfg)
        with db.atomic():
            record.save()
        return {
            "success": True,
            "data": [record.list_item()]
        }

    @api
    def update_item(self, cfg):
        with db.atomic():
            try:
                record = self.model.get(self.model.id == int(cfg["id"]))
            except peewee.DoesNotExist:
                return {
                    "success": False
                }
            for f in cfg:
                if f == "id":
                    continue
                setattr(record, f, cfg[f])
            record.save()
            return {
                "success": True,
                "data": [record.list_item()]
            }

    @api
    def delete_item(self, cfg):
        with db.atomic():
            try:
                record = self.model.get(self.model.id == int(cfg["id"]))
            except peewee.DoesNotExist:
                return {
                    "success": False
                }
            record.delete_instance()
            return {
                "success": True
            }
