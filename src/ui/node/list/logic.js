// ----------------------------------------------------------------------
// Node List logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { app_logic } from "../../app/logic.js";
import { Route, router } from "../../route.js";

export class NodeListLogic {
    on_route = async (env_id) => {
        await app_logic.with_environment(parseInt(env_id, 10));
        $$("node_list_panel").show();
        this.load();
    };

    // Load data info list
    load = () => {
        $$("node_list").load("rpc->node");
    };

    on_search = (nv, ov) => {
        console.log("Search", nv, ov);
    };
};
export const node_list_logic = new NodeListLogic();
router.push(
    new Route(/^\/environment\/(\d+)\/node$/, node_list_logic.on_route, "node"),
);