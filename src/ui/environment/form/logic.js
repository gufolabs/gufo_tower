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
import { copyToClipboard } from "../../clipboard.js";

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
    };

    on_route_item = async (env_id) => {
        try {
            const data = await API.environment.get_item({
                id: parseInt(env_id, 10)
            });
            current_env.setState(data);
            $$("environment_form").setValues(data);
            $$("environment_form_panel").show();
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
            const confirmed = await webix.confirm({
                title: "Delete environment?",
                text: "Are you sure you want to delete this environment?<br><br>" +
                    "This operation cannot be undone.",
                type: "confirm-error",
            });
            if (!confirmed) {
                return;
            }
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

    on_copy_key = async () => {
        let key;
        try {
            key = await API.environment.get_ssh_public_key(current_env.state.id);
        } catch {
            Tower.msg.failed("Failed to get key");
            return;
        }
        if (key === "") {
            Tower.msg.failed("No key configured");
            return;
        }
        await copyToClipboard(key);
    }
};

export const environment_form_logic = new EnvironmentFormLogic();

router.push(
    new Route(/^\/environment\/new$/, environment_form_logic.on_route_new, "environment"),
    new Route(/^\/environment\/(\d+)$/, environment_form_logic.on_route_item, "environment")
);