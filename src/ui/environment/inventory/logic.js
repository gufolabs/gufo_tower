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

    on_route = async (e_id) => {
        const env_id = parseInt(e_id, 10);

        try {
            await app_logic.with_environment(env_id);
            const result = await API.environment.ansible_inventory(env_id);
            $$("environment_inventory_text").setValues({
                text: result
            });
            $$("environment_inventory_panel").show();
        } catch {
            Tower.msg.failed("Cannot get inventory");
        }
    };
};

export const environment_inventory_logic = new EnvironmentInventoryLogic();

export const environment_inventory_routes = [
    new Route(/^\/environment\/(\d+)\/inventory$/, environment_inventory_logic.on_route, "environment"),
];