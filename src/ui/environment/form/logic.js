// ----------------------------------------------------------------------
// Environment Form logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route } from "../../route.js";

export class EnvironmentFormLogic {
    init = () => {
    };

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

    on_route_item = (env_id) => {
        return API.environment.get_item({ id: parseInt(env_id, 10) })
            .then((data) => {
                $$("environment_form").setValues(data);
                $$("environment_form_panel").show();
                return API.pull.is_pulled(data.id);
            })
            .then((result) => {
                if (result) {
                    $$("pulled_label").setHTML("...");
                } else {
                    $$("pulled_label").setHTML("");
                }
            })
            .catch((err) => {
                Tower.msg.failed("Failed to get data");
            });
    };

    on_save = () => {
        let data;
        const form = $$("environment_form");

        if (form.validate()) {
            data = form.getValues();
            if (data.id === undefined) {
                API.environment.create_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        navigation.navigate("/environment")
                        Tower.msg.complete("Created");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to create " + err);
                    }
                );
            } else {
                API.environment.update_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        navigation.navigate("/environment")
                        Tower.msg.complete("Changed");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to change" + err);
                    }
                );
            }
        } else {
            Tower.msg.failed("Error in data");
        }
    };

    on_delete = () => {
        const data = $$("environment_form").getValues();
        if (data.id) {
            API.environment.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("environment_list").remove(data.id);
                    // @todo: Unselect environment
                    navigation.navigate("/environment")
                },
                function () {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            navigation.navigate("/environment")
        }
    };
};

export const environment_form_logic = new EnvironmentFormLogic();

export const environment_form_routes = [
    new Route(/^\/environment\/new$/, environment_form_logic.on_route_new, "environment"),
    new Route(/^\/environment\/(\d+)$/, environment_form_logic.on_route_item, "environment"),
];