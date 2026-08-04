// ----------------------------------------------------------------------
// Main entrypoint
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import "./style.css";
import "./skin.js";
import "./rpc.js";
import "./lib.js";
import "./login_ui.js";
import "./login_logic.js";
import "./change_password_ui.js";
import "./change_password_logic.js";
import "./environment_ui.js";
import "./environment_logic.js";
import "./datacenter_ui.js";
import "./datacenter_logic.js";
import "./role_ui.js";
import "./role_logic.js";
import "./pool_ui.js";
import "./pool_logic.js";
import "./node_ui.js";
import "./node_logic.js";
import "./service_ui.js";
import "./service_logic.js";
import "./settings_ui.js";
import "./settings_logic.js";
import "./desktop_ui.js";
import "./desktop_logic.js";
import { app_ui } from "./app_ui.js";
import { app_logic } from "./app_logic.js";
import { login_logic } from "./login_logic.js";
import { change_password_logic } from "./change_password_logic.js";
import { desktop_logic } from "./desktop_logic.js";

function init() {
    webix.ui(app_ui);

    login_logic.init();
    change_password_logic.init();
    desktop_logic.init();

    app_logic.process_login();
}
webix.ready(init);