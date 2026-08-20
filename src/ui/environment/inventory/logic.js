// ----------------------------------------------------------------------
// Environment Inventory logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route, router } from "../../route.js";
import { current_env } from "../../state.js";

export class EnvironmentInventoryLogic {
    on_route = async (e_id) => {
        const env_id = parseInt(e_id, 10);

        try {
            await current_env.with(env_id);
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

router.push(
    new Route(/^\/environment\/(\d+)\/inventory$/, environment_inventory_logic.on_route, "environment")
);