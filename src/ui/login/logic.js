// ----------------------------------------------------------------------
// Login logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../rpc.js";
import { desktop_logic } from "../desktop/logic.js";
import { Tower } from "../lib.js";
import { Route, router } from "../route.js";
import { state } from "../state.js";

export class LoginLogic {
    init = () => {
    };

    on_route = () => {
        $$("login_panel").show();
        this.clear_form();
    };

    clear_form = () => {
        $$("login_form").clear();
        $$("login_form").focus("user");
    };

    on_login = () => {
        if (!$$("login_form").validate()) {
            return;
        }
        const data = $$("login_form").getValues();
        this.login(data.user, data.password);
    };

    login = async (user, password) => {
        try {
            const result = await API.login.login({
                user: user,
                password: password
            });
            if (result) {
                desktop_logic.show();
                navigation.navigate(state.pop_return_path());
            } else {
                Tower.msg.failed("Login failed");
            }
        } catch {
            Tower.msg.failed("Connection failed");
        }
    };
};
export const login_logic = new LoginLogic();

router.push(
    new Route(/^\/login$/, login_logic.on_route)
);