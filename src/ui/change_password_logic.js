// ----------------------------------------------------------------------
// Change password logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "./rpc.js";
import { desktop_logic } from "./desktop_logic.js";
import { Tower } from "./lib.js";

export const change_password_logic = {
    init: function () {
    },

    show: function () {
        $$("change_password_panel").show();
        change_password_logic.clear_form();
    },

    clear_form: function () {
        $$("change_password_form").clear();
        $$("change_password_form").focus("old_password");
    },

    on_change_password: function () {
        if (!$$("change_password_form").validate()) {
            return;
        }
        const data = $$("change_password_form").getValues();
        if (data.new_password !== data.new_password2) {
            Tower.msg.failed("Passwords mismatch");
            return;
        }
        API.login.change_password(data.old_password, data.new_password).then(
            function () {
                Tower.msg.complete("Password changed");
                desktop_logic.show();
            },
            function () {
                Tower.msg.failed("Failed to change password");
            }
        );
    }
};
