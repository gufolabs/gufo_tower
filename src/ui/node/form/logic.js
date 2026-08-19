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

    on_route_new = async (env_id) => {
        await app_logic.with_environment(parseInt(env_id, 10));
        $$("node_form").clear();
        $$("node_form_panel").show();
    };
    on_route_item = async (env_id, node_id) => {
        try {
            await app_logic.with_environment(parseInt(env_id, 10));

            const data = await API.node.get_item({
                id: parseInt(node_id, 10)
            });

            $$("node_form").setValues(data);
            $$("node_form_panel").show();
        } catch {
            Tower.msg.failed("Failed to get data");
        }
    };
    on_save = async () => {
        const form = $$("node_form");

        if (!form.validate()) {
            Tower.msg.failed("Error in data");
            return;
        }

        const data = form.getValues();
        data.environment = app_logic.current_env.id;

        try {
            if (data.id === undefined) {
                const result = await API.node.create_item(data);
                form.setValues(result);
                form.save();
                navigation.navigate("..");
                Tower.msg.complete("Created");
            } else {
                const result = await API.node.update_item(data);
                form.setValues(result);
                form.save();
                navigation.navigate("..");
                Tower.msg.complete("Changed");
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
        const data = $$("node_form").getValues();

        if (data.id) {
            try {
                await API.node.delete_item(data);
                Tower.msg.complete("Deleted");
                $$("node_list").remove(data.id);
                navigation.navigate("..");
            } catch {
                Tower.msg.failed("Failed to delete");
            }
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