// ----------------------------------------------------------------------
// Login logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../rpc.js";
import { desktop_logic } from "../desktop/logic.js";
import { Tower } from "../lib.js";
import { Route } from "../route.js";

export class LoginLogic {
    init = () => {
    };

    on_route = () => {
        $$("login_panel").show();
        login_logic.clear_form();
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
        login_logic.login(data.user, data.password);
    };

    login = (user, password) => {
        API.login.login({
            user: user,
            password: password
        }).then(function (result) {
            if (result) {
                desktop_logic.show();
            } else {
                Tower.msg.failed("Login failed");
            }
        }, function (err) {
            Tower.msg.failed("Connection failed");
        });
    };
};
export const login_logic = new LoginLogic();

export const login_routes = [
    new Route(/^\/login$/, login_logic.on_route),
];