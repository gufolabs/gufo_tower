// ----------------------------------------------------------------------
// Desktop logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { environment_logic } from "./environment_logic.js";
import { datacenter_logic } from "./datacenter_logic.js";
import { role_logic } from "./role_logic.js";
import { pool_logic } from "./pool_logic.js";
import { app_logic } from "./app_logic.js";
import { node_logic } from "./node_logic.js";
import { service_logic } from "./service_logic.js";
import { change_password_logic } from "./change_password_logic.js";
import { Tower } from "./lib.js";
import { settings_logic } from "./settings_logic.js";

export const desktop_logic = {
    init: function () {
        Object.values(this.apps).forEach(app => app.init());
    },

    apps: {
        environment: environment_logic,
        datacenter: datacenter_logic,
        role: role_logic,
        pool: pool_logic,
        node: node_logic,
        service: service_logic,
        settings: settings_logic,
    },

    show: function () {
        $$("desktop").show();
        $$("sidebar").select("environment");
    },

    on_before_select_app: function (app) {
        const can_run = this.apps[app]?.can_run?.() ?? true;
        if (!can_run) {
            Tower.msg.failed("Select environment");
        }
        return can_run;
    },

    on_select_app: function (selection) {
        this.apps[selection[0]]?.show();
    },

    select_environment: function (env) {
        $$("environment_label").setValue("NOC Tower: " + env.name);
    },

    on_menu_click: function (item_id) {
        switch (item_id) {
            case "docs":
                window.open("/docs/index.html", "_blank");
                break;
            case "logout":
                app_logic.logout();
                break;
            case "change_password":
                change_password_logic.show();
                break;
            default:
                break;
        }
    }
};
