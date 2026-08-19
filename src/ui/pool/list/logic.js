// ----------------------------------------------------------------------
// Pool logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { Route } from "../../route.js";
import { app_logic } from "../../app/logic.js";

export class PoolListLogic {
    init = () => {
    };

    on_route = async (env_id) => {
        await app_logic.with_environment(parseInt(env_id, 10));
        $$("pool_list_panel").show();
        this.load();
    };

    // Load data info list
    load = () => {
        $$("pool_list").load("rpc->pool");
    };

    on_search = (nv, ov) => {
    };
};

export const pool_list_logic = new PoolListLogic();
export const pool_list_routes = [
    new Route(/^\/environment\/(\d+)\/pool$/, pool_list_logic.on_route, "pool"),
];