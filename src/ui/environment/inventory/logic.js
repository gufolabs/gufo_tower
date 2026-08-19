// ----------------------------------------------------------------------
// Environment Inventory logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route } from "../../route.js";
import { app_logic } from "../../app/logic.js";

export class EnvironmentInventoryLogic {
    init = () => {
    };

    on_route = (e_id) => {
        const env_id = parseInt(e_id, 10);
        return app_logic.with_environment(env_id)
            .then(() => API.environment.ansible_inventory(env_id))
            .then((result) => {
                $$("environment_inventory_text").setValues({
                    text: result
                });
                $$("environment_inventory_panel").show();
            })
            .catch((err) => {
                Tower.msg.failed("Cannot get inventory");
            });
    };
};

export const environment_inventory_logic = new EnvironmentInventoryLogic();

export const environment_inventory_routes = [
    new Route(/^\/environment\/(\d+)\/inventory$/, environment_inventory_logic.on_route, "environment"),
];