// ----------------------------------------------------------------------
// Node Form logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { app_logic } from "../../app/logic.js";
import { Tower } from "../../lib.js";
import { Route } from "../../route.js";

export class NodeFormLogic {
    init = () => {
    };

    on_route_new = (env_id) => {
        return app_logic.with_environment(parseInt(env_id, 10)).then(() => {
            $$("node_form").clear();
            $$("node_form_panel").show();
        });
    };

    on_route_item = (env_id, node_id) => {
        return app_logic.with_environment(parseInt(env_id, 10))
            .then(() => API.node.get_item({ id: parseInt(node_id, 10) }))
            .then(
                (data) => {
                    $$("node_form").setValues(data);
                    $$("node_form_panel").show();
                })
            .catch(() => {
                Tower.msg.failed("Failed to get data");
            });
    };

    on_save = () => {
        let data;
        const form = $$("node_form");

        if (form.validate()) {
            data = form.getValues();
            data.environment = app_logic.current_env.id;
            if (data.id === undefined) {
                API.node.create_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        navigation.navigate("..");
                        Tower.msg.complete("Created");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to create " + err);
                    }
                );
            } else {
                API.node.update_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        navigation.navigate("..");
                        Tower.msg.complete("Changed");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to change " + err);
                    }
                );
            }
        } else {
            Tower.msg.failed("Error in data");
        }
    };

    on_delete = () => {
        const data = $$("node_form").getValues();
        if (data.id) {
            API.node.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("node_list").remove(data.id);
                    navigation.navigate("..");
                },
                function () {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            navigation.navigate("..");
        }
    };
};

export const node_form_logic = new NodeFormLogic();
export const node_form_routes = [
    new Route(/^\/environment\/(\d+)\/node\/new$/, node_form_logic.on_route_new, "node"),
    new Route(/^\/environment\/(\d+)\/node\/(\d+)$/, node_form_logic.on_route_item, "node"),
]