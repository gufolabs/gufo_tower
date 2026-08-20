// ----------------------------------------------------------------------
// Change password logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../rpc.js";
import { Tower } from "../lib.js";
import { Route, router } from "../route.js";

export class ChangePasswordLogic {
    init = () => {
    };

    on_route = () => {
        $$("change_password_panel").show();
        change_password_logic.clear_form();
    };

    clear_form = () => {
        $$("change_password_form").clear();
        $$("change_password_form").focus("old_password");
    };

    on_change_password = async () => {
        if (!$$("change_password_form").validate()) {
            return;
        }
        const data = $$("change_password_form").getValues();
        if (data.new_password !== data.new_password2) {
            Tower.msg.failed("Passwords mismatch");
            return;
        }
        try {
            await API.login.change_password(data.old_password, data.new_password);
            Tower.msg.complete("Password changed");
            navigation.navigate("/");
        } catch {
            Tower.msg.failed("Failed to change password");
        }
    };
};

export const change_password_logic = new ChangePasswordLogic();

router.push(
    new Route(/^\/change-password$/, change_password_logic.on_route)
);