// ----------------------------------------------------------------------
// Environment Form logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route, router } from "../../route.js";
import { current_env } from "../../state.js";

export class EnvironmentFormLogic {
    on_route_new = () => {
        $$("environment_form_panel").show();
        $$("environment_form").clear();
        $$("environment_form").setValues({
            env_type: "eval",
            install_method: "git",
            playbook_link: "git+https://github.com/gufolabs/noc@stable",
            installation_name: "Unconfigured installation",
            config_order: "yaml:///opt/noc/etc/tower.yml,yaml:///opt/noc/etc/settings.yml,env:///NOC",
            name: "NOC"
        });
        $$("pulled_label").setHTML("");
    };

    on_route_item = async (env_id) => {
        try {
            const data = await API.environment.get_item({
                id: parseInt(env_id, 10)
            });

            $$("environment_form").setValues(data);
            $$("environment_form_panel").show();

            const result = await API.pull.is_pulled(data.id);

            if (result) {
                $$("pulled_label").setHTML("...");
            } else {
                $$("pulled_label").setHTML("");
            }
        } catch {
            Tower.msg.failed("Failed to get data");
        }
    };

    to_list = () => {
        navigation.navigate("/environment");
    };

    on_save = async () => {
        const form = $$("environment_form");
        if (!form.validate()) {
            Tower.msg.failed("Error in data");
            return;
        }
        const data = form.getValues();
        try {
            if (data.id === undefined) {
                const result = await API.environment.create_item(data);
                this.to_list();
                Tower.msg.complete("Created");
                current_env.setState(result);
            } else {
                const result = await API.environment.update_item(data);
                this.to_list();
                Tower.msg.complete("Changed");
                current_env.setState(result);
            }
        } catch (err) {
            if (data.id === undefined) {
                Tower.msg.failed("Failed to create " + err);
            } else {
                Tower.msg.failed("Failed to change " + err);
            }
        }
    };

    on_delete = async () => {
        const data = $$("environment_form").getValues();

        if (data.id) {
            try {
                await API.environment.delete_item(data);
                Tower.msg.complete("Deleted");
                $$("environment_list").remove(data.id);
                // @todo: Unselect environment
                this.to_list();
            } catch {
                Tower.msg.failed("Failed to delete");
            }
        } else {
            Tower.msg.complete("Deleted");
            current_env.setState(null);
            this.to_list();
        }
    };
};

export const environment_form_logic = new EnvironmentFormLogic();

router.push(
    new Route(/^\/environment\/new$/, environment_form_logic.on_route_new, "environment"),
    new Route(/^\/environment\/(\d+)$/, environment_form_logic.on_route_item, "environment")
);