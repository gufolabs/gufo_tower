// ----------------------------------------------------------------------
// Main entrypoint
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import "./style.css";
import "./skin.js";
import "./login/ui.js";
import "./change_password/ui.js";
import "./desktop/ui.js";
import { API } from "./rpc.js";
import { Tower } from "./lib.js";
import { app_ui } from "./app/ui.js";
import { app_logic } from "./app/logic.js";
import { change_password_logic, change_password_routes } from "./change_password/logic.js";
import { desktop_logic } from "./desktop/logic.js";
import { Router } from "./router.js";
import { login_routes, login_logic } from "./login/logic.js";
import { home_routes } from "./home/logic.js";
import { environment_list_routes } from "./environment/list/logic.js";
import { environment_form_routes } from "./environment/form/logic.js";
import { environment_inventory_routes } from "./environment/inventory/logic.js";
import { environment_deploy_routes } from "./environment/deploy/logic.js";
import { datacenter_list_routes } from "./datacenter/list/logic.js";
import { datacenter_form_routes } from "./datacenter/form/logic.js";
import { pool_list_routes } from "./pool/list/logic.js";
import { pool_form_routes } from "./pool/form/logic.js";
import { node_list_routes } from "./node/list/logic.js";
import { node_form_routes } from "./node/form/logic.js";
import { role_list_routes } from "./role/list/logic.js";
import { role_form_routes } from "./role/form/logic.js";
import { service_routes } from "./service/logic.js";
import { settings_routes } from "./settings/logic.js";

const router = new Router([
    ...home_routes,
    ...login_routes,
    ...change_password_routes,
    ...environment_list_routes,
    ...environment_form_routes,
    ...environment_inventory_routes,
    ...environment_deploy_routes,
    ...datacenter_list_routes,
    ...datacenter_form_routes,
    ...pool_list_routes,
    ...pool_form_routes,
    ...node_list_routes,
    ...node_form_routes,
    ...service_routes,
    ...role_list_routes,
    ...role_form_routes,
    ...settings_routes,
]);

async function init() {
    webix.ui(app_ui);

    router.init();
    app_logic.init();
    login_logic.init();
    change_password_logic.init();
    desktop_logic.init();
    try {
        const result = await API.login.is_logged();
        if (result) {
            desktop_logic.show();
            await router.show(window.location.pathname);
        } else {
            navigation.navigate("/login");
        }
    } catch {
        Tower.msg.failed("Failed to connect to server");
        navigation.navigate("/login");
    }
}

webix.ready(init);