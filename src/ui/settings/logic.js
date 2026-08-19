// ----------------------------------------------------------------------
// Settings logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../rpc.js";
import { Tower } from "../lib.js";
import { Route } from "../route.js";

export class SettingsLogic {
    init = () => {
    };

    on_route = () => {
        this.show();
    };

    show = () => {
        $$("settings_form_panel").show();
        API.settings.get_settings().then(function (result) {
            $$("settings_form").setValues(result);
        }).fail(function (err) {
            Tower.msg.failed("Failed to get settings")
        });
    };

    on_save = () => {
        const form = $$("settings_form");
        if (form.validate()) {
            API.settings.save_settings(form.getValues()).then(
                function () {
                    Tower.msg.complete("Settings saved");
                }, function () {
                    Tower.msg.failed("Failed to save settings");
                }
            );
        } else {
            Tower.msg.failed("Error in settings");
        }
    };
};
export const settings_logic = new SettingsLogic();

export const settings_routes = [
    new Route(/^\/settings$/, settings_logic.on_route, "settings")
];