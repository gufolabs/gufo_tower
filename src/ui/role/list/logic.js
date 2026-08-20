// ----------------------------------------------------------------------
// Role List logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { app_logic } from "../../app/logic.js";
import { Route, router } from "../../route.js";

export class RoleListLogic {
    on_route = async (env_id) => {
        await app_logic.with_environment(parseInt(env_id, 10));
        $$("role_list_panel").show();
        this.load();
    };

    // Load data info list
    load = () => {
        $$("role_list").load("rpc->role");
    };

    on_search = (nv, ov) => {
        console.log("Search", nv, ov);
    };
};

export const role_list_logic = new RoleListLogic();

router.push(
    new Route(/^\/environment\/(\d+)\/role$/, role_list_logic.on_route, "role")
);