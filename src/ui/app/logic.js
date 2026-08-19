// ----------------------------------------------------------------------
// Application logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../rpc.js";
import { desktop_logic } from "../desktop/logic.js";
import { Tower } from "../lib.js";

export class AppLogic {
    current_env = null;

    init = () => { };

    select_environment = (env) => {
        app_logic.current_env = env;
        desktop_logic.select_environment(env);
    };

    with_environment = (env_id) => {
        return API.environment.get_item({ id: env_id }).then(
            (env) => {
                this.select_environment(env);
                return env;
            },
            (err) => {
                Tower.msg.failed("Failed to get environment");
                throw err;
            }
        );
    };

    is_environment_selected = () => {
        return app_logic.current_env !== null;
    };

    logout = () => {
        API.login.logout().then(
            function () {
                navigation.navigate("/login");
                Tower.msg.complete("Logged out");
            },
            function () {
                Tower.msg.failed("Failed to log out");
            }
        );
    };
};

export const app_logic = new AppLogic();