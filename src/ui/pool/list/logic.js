// ----------------------------------------------------------------------
// Pool logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { Route, router } from "../../route.js";
import { app_logic } from "../../app/logic.js";

export class PoolListLogic {
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
router.push(
    new Route(/^\/environment\/(\d+)\/pool$/, pool_list_logic.on_route, "pool")
);