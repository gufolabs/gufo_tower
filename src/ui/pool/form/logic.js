// ----------------------------------------------------------------------
// Pool logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route, router } from "../../route.js";
import { current_env } from "../../state.js";

export class PoolFormLogic {
    on_route_new = async (env_id) => {
        await current_env.with(parseInt(env_id, 10));
        $$("pool_form").clear();
        $$("pool_form_panel").show();
    };

    on_route_item = async (env_id, pool_id) => {
        try {
            await current_env.with(parseInt(env_id, 10));

            const data = await API.pool.get_item({
                id: parseInt(pool_id, 10)
            });

            $$("pool_form").setValues(data);
            $$("pool_form_panel").show();
        } catch {
            Tower.msg.failed("Failed to get data");
        }
    };
    to_list = () => {
        navigation.navigate(`/environment/${current_env.state.id}/pool`);
    }
    on_save = async () => {
        const form = $$("pool_form");
        if (!form.validate()) {
            Tower.msg.failed("Error in data");
            return;
        }
        const data = form.getValues();
        data.environment = current_env.state.id;
        try {
            if (data.id === undefined) {
                await API.pool.create_item(data);
                this.to_list();
                Tower.msg.complete("Created");
            } else {
                await API.pool.update_item(data);
                this.to_list();
                Tower.msg.complete("Changed");
            }
        } catch {
            if (data.id === undefined) {
                Tower.msg.failed("Failed to create");
            } else {
                Tower.msg.failed("Failed to change");
            }
        }
    };

    on_delete = async () => {
        const data = $$("pool_form").getValues();

        if (data.id) {
            try {
                await API.pool.delete_item(data);
                Tower.msg.complete("Deleted");
                $$("pool_list").remove(data.id);
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

export const pool_form_logic = new PoolFormLogic();
router.push(
    new Route(/^\/environment\/(\d+)\/pool\/new$/, pool_form_logic.on_route_new, "pool"),
    new Route(/^\/environment\/(\d+)\/pool\/(\d+)$/, pool_form_logic.on_route_item, "pool"),
);