# ----------------------------------------------------------------------
# Settings API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from ..models.settings import Settings
from .base import API, api, open_api


class SettingsAPI(API):
    name = "settings"

    @api
    def get_settings(self):
        """Returns a list of current settings."""
        r = Settings.DEFAULTS.copy()
        r["url"] = "http://{}/".format(self.handler.request.headers["Host"])
        r.update(Settings.get_items(list(Settings.DEFAULTS)))
        return r

    @api
    def save_settings(self, data):
        """Save current settings."""
        current = Settings.get_items(list(Settings.DEFAULTS))
        for k in data:
            if k not in Settings.DEFAULTS:
                continue
            if k not in current or current[k] != data[k]:
                Settings.set_item(k, data[k])
        return True

    @open_api
    def app_config(self):
        """Get application config."""
        return {"installation_name": Settings.get_installation_name()}
