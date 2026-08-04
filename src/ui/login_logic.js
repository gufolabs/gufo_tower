// ----------------------------------------------------------------------
// Login logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "./rpc.js";
import { desktop_logic } from "./desktop_logic.js";
import { Tower } from "./lib.js";

export const login_logic = {
    init: function () {
    },

    show: function () {
        $$("login_panel").show();
        login_logic.clear_form();
    },

    clear_form: function () {
        $$("login_form").clear();
        $$("login_form").focus("user");
    },

    on_login: function () {
        var data;
        if (!$$("login_form").validate()) {
            return;
        }
        data = $$("login_form").getValues();
        login_logic.login(data.user, data.password);
    },

    login: function (user, password) {
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
    },

    logout: function () {
        API.login.logout().then(function (result) {
            login_logic.show();
        });
    }
};
