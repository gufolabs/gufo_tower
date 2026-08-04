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

export const desktop_logic = {
    init: function () {
        environment_logic.init();
        datacenter_logic.init();
        role_logic.init();
        pool_logic.init();
        node_logic.init();
        service_logic.init();
    },

    show: function () {
        $$("desktop").show();
        $$("sidebar").select("environment");
    },

    on_before_select_app: function (app) {
        var logic = window[app + "_logic"],
            can_run = true;
        if (logic && logic.can_run) {
            can_run = logic.can_run();
        }
        if (!can_run) {
            Tower.msg.failed("Select environment");
        }
        return can_run;
    },

    on_select_app: function (selection) {
        var logic = window[selection[0] + "_logic"];
        if (logic) {
            logic.show();
        }
    },

    select_environment: function (env) {
        $$("environment_label").setValue("NOC Tower: " + env.name);
    },

    on_menu_click: function (item_id) {
        switch (item_id) {
            case "logout":
                app_logic.logout();
                break;
            case "change_password":
                change_password_logic.show();
                break;
        }
    }
};
