// ----------------------------------------------------------------------
// Tower entrypont
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE for details
// ----------------------------------------------------------------------

import "./style.css";
import "./skin.js";
import "./rpc.js";
import "./lib.js";
import "./config.js";
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
import "./app_ui.js";
import "./app_logic.js";
import { app_logic } from "./app_logic.js";

webix.ready(app_logic.init);