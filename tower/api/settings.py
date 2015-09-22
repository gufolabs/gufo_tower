# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Settings API
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Tower modules
from base import API, api
from tower.models.settings import Settings


class SettingsAPI(API):
    name = "Settings"

    DEFAULTS = {
        "url": "http://example.com/"
    }

    @api
    def get_settings(self):
        """
        Returns a list of current settings
        :return:
        """
        r = self.DEFAULTS.copy()
        r.update(Settings.get_items(list(self.DEFAULTS)))
        return r

    @api
    def save_settings(self, data):
        """
        Save current settings
        :return:
        """
        current = Settings.get_items(list(self.DEFAULTS))
        for k in data:
            if k not in self.DEFAULTS:
                continue
            if k not in current or current[k] != data[k]:
                Settings.set_item(k, data[k])
        return {
            "success": True
        }
