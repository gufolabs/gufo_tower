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

    on_route = async () => {
        $$("settings_form_panel").show();
        try {
            const result = await API.settings.get_settings();
            $$("settings_form").setValues(result);
        } catch {
            Tower.msg.failed("Failed to get settings");
        }
    };

    on_save = async () => {
        const form = $$("settings_form");
        if (!form.validate()) {
            Tower.msg.failed("Error in settings");
            return;
        }
        try {
            await API.settings.save_settings(form.getValues());
            Tower.msg.complete("Settings saved");
        } catch {
            Tower.msg.failed("Failed to save settings");
        }
    };
};
export const settings_logic = new SettingsLogic();

export const settings_routes = [
    new Route(/^\/settings$/, settings_logic.on_route, "settings")
];