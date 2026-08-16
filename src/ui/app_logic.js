// ----------------------------------------------------------------------
// Application logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "./rpc.js";
import { login_logic } from "./login_logic.js";
import { desktop_logic } from "./desktop_logic.js";
import { Tower } from "./lib.js";

export class AppLogic {
    current_env = null;

    process_login = () => {
        // Check user is logged in
        API.login.is_logged().then(
            function (result) {
                if (result) {
                    desktop_logic.show();
                } else {
                    login_logic.show();
                }
            }, function (err) {
                Tower.msg.failed("Failed to connect to server");
                login_logic.show();
            }
        );
    };

    select_environment = (env) => {
        app_logic.current_env = env;
        desktop_logic.select_environment(env);
    };

    is_environment_selected = () => {
        return app_logic.current_env !== null;
    };

    logout = () => {
        API.login.logout().then(
            function () {
                login_logic.show();
                Tower.msg.complete("Logged out");
            },
            function () {
                Tower.msg.failed("Failed to log out");
            }
        );
    };
};

export const app_logic = new AppLogic();