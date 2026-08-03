import { API } from "./rpc.js";
import { login_logic } from "./login_logic.js";
import { desktop_logic } from "./desktop_logic.js";

export const app_logic = {
    current_env: null,

    process_login: function () {
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
    },

    select_environment: function (env) {
        app_logic.current_env = env;
        desktop_logic.select_environment(env);
    },

    is_environment_selected: function () {
        return app_logic.current_env !== null;
    },

    logout: function () {
        API.login.logout().then(
            function () {
                login_logic.show();
                Tower.msg.complete("Logged out");
            },
            function () {
                Tower.msg.failed("Failed to log out");
            }
        );
    }
};
