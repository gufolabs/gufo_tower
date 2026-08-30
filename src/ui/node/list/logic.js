// ----------------------------------------------------------------------
// Node List logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Route, router } from "../../route.js";
import { Tower } from "../../lib.js";
import { current_env } from "../../state.js";

export class NodeListLogic {
    on_route = async (env_id) => {
        await current_env.with(parseInt(env_id, 10));
        $$("node_list_panel").show();
        this.load();
    };

    // Load data info list
    load = () => {
        $$("node_list").load("rpc->node");
    };

    on_inventory = async () => {
        const nodeIds = $$("node_list")
            .serialize()
            .map(({ id }) => id);
        Tower.msg.started("Updating inventory");
        try {
            await API.node.update_facts(nodeIds);
            Tower.msg.complete("Inventory updated");
            this.load();
        } catch {
            Tower.msg.failed("Failed to get inventory");
        }
    }

    on_search = (nv, ov) => {
        console.log("Search", nv, ov);
    };
};
export const node_list_logic = new NodeListLogic();
router.push(
    new Route(/^\/environment\/(\d+)\/node$/, node_list_logic.on_route, "node"),
);