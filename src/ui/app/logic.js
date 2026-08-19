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

    with_environment = async (env_id) => {
        try {
            const env = await API.environment.get_item({ id: env_id });
            this.select_environment(env);
            return env;
        } catch (err) {
            Tower.msg.failed("Failed to get environment");
            throw err;
        }
    };

    is_environment_selected = () => {
        return app_logic.current_env !== null;
    };

    logout = async () => {
        try {
            await API.login.logout();
            navigation.navigate("/login");
            Tower.msg.complete("Logged out");
        } catch {
            Tower.msg.failed("Failed to log out");
        }
    };
};

export const app_logic = new AppLogic();