// ----------------------------------------------------------------------
// Node Form logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route, router } from "../../route.js";
import { current_env } from "../../state.js";

export class NodeFormLogic {
    on_route_new = async (env_id) => {
        await current_env.with(parseInt(env_id, 10));
        await this.load_lookups();
        $$("node_form").clear();
        $$("node_form_panel").show();
    };
    on_route_item = async (env_id, node_id) => {
        try {
            await current_env.with(parseInt(env_id, 10));

            const data = await API.node.get_item({
                id: parseInt(node_id, 10)
            });
            await this.load_lookups();

            $$("node_form").setValues(data);
            $$("node_form_panel").show();
        } catch {
            Tower.msg.failed("Failed to get data");
        }
    };
    load_lookups = async () => {
        console.log("load lookups");
        const [datacenters, node_types] = await Promise.all([
            API.datacenter.lookup_items({}),
            API.nodetype.lookup_items({}),
        ]);
        console.log(datacenters, node_types);
        $$("node_form").elements.datacenter.define("options", datacenters.data);
        $$("node_form").elements.node_type.define("options", node_types.data);
    };
    to_list = () => {
        navigation.navigate(`/environment/${current_env.state.id}/node`);
    };
    on_save = async () => {
        const form = $$("node_form");
        if (!form.validate()) {
            Tower.msg.failed("Error in data");
            return;
        }
        const data = form.getValues();
        data.environment = current_env.state.id;
        try {
            if (data.id === undefined) {
                await API.node.create_item(data);
                this.to_list();
                Tower.msg.complete("Created");
            } else {
                await API.node.update_item(data);
                this.to_list();
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
            const confirmed = await webix.confirm({
                title: "Delete node?",
                text: "Are you sure you want to delete this node?<br><br>" +
                    "This operation cannot be undone.",
                type: "confirm-error",
            });
            if (!confirmed) {
                return;
            }
            try {
                await API.node.delete_item(data);
                Tower.msg.complete("Deleted");
                $$("node_list").remove(data.id);
                this.to_list();
            } catch {
                Tower.msg.failed("Failed to delete");
            }
        } else {
            Tower.msg.complete("Deleted");
            this.to_list();
        }
    };
};

export const node_form_logic = new NodeFormLogic();
router.push(
    new Route(/^\/environment\/(\d+)\/node\/new$/, node_form_logic.on_route_new, "node"),
    new Route(/^\/environment\/(\d+)\/node\/(\d+)$/, node_form_logic.on_route_item, "node")
);