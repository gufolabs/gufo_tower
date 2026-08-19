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
import { state } from "./state.js";
import { router } from "./route.js";
import { app_logic } from "./app/logic.js";
import { change_password_logic } from "./change_password/logic.js";
import { desktop_logic } from "./desktop/logic.js";
import { login_logic } from "./login/logic.js";
// Import application modules to register their routes.
import "./home/logic.js";
import "./environment/list/logic.js";
import "./environment/form/logic.js";
import "./environment/inventory/logic.js";
import "./environment/deploy/logic.js";
import "./datacenter/list/logic.js";
import "./datacenter/form/logic.js";
import "./pool/list/logic.js";
import "./pool/form/logic.js";
import "./node/list/logic.js";
import "./node/form/logic.js";
import "./role/list/logic.js";
import "./role/form/logic.js";
import "./service/logic.js";
import "./settings/logic.js";

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
            await router.show();
        } else {
            state.push_return_path();
            navigation.navigate("/login");
        }
    } catch {
        Tower.msg.failed("Failed to connect to server");
        navigation.navigate("/login");
    }
}

webix.ready(init);