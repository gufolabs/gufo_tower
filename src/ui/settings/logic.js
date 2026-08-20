// ----------------------------------------------------------------------
// Settings logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../rpc.js";
import { Tower } from "../lib.js";
import { Route, router } from "../route.js";
import { installation_name } from "../state.js";

export class SettingsLogic {
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
            const values = form.getValues();
            await API.settings.save_settings(values);
            Tower.msg.complete("Settings saved");
            installation_name.setState(values.installation_name);
        } catch {
            Tower.msg.failed("Failed to save settings");
        }
    };
};
export const settings_logic = new SettingsLogic();

router.push(
    new Route(/^\/settings$/, settings_logic.on_route, "settings")
);