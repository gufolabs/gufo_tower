// ----------------------------------------------------------------------
// Pool logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { app_logic } from "../../app/logic.js";
import { Tower } from "../../lib.js";
import { Route } from "../../route.js";

export class PoolFormLogic {
    init = () => {
    };

    on_route_new = (env_id) => {
        return app_logic.with_environment(parseInt(env_id, 10)).then(() => {
            $$("pool_form").clear();
            $$("pool_form_panel").show();
        });
    }

    on_route_item = (env_id, pool_id) => {
        return app_logic.with_environment(parseInt(env_id, 10))
            .then(() => API.pool.get_item({ id: parseInt(pool_id, 10) }))
            .then((data) => {
                $$("pool_form").setValues(data);
                $$("pool_form_panel").show();
            })
            .catch((err) => {
                Tower.msg.failed("Failed to get data");
            });
    }

    on_save = () => {
        let data;
        const form = $$("pool_form");

        if (form.validate()) {
            data = form.getValues();
            data.environment = app_logic.current_env.id;
            if (data.id === undefined) {
                API.pool.create_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        navigation.navigate("..");
                        Tower.msg.complete("Created");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to create");
                    }
                );
            } else {
                API.pool.update_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        navigation.navigate("..");
                        Tower.msg.complete("Changed");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to change");
                    }
                );
            }
        } else {
            Tower.msg.failed("Error in data");
        }
    };

    on_delete = () => {
        const data = $$("pool_form").getValues();
        if (data.id) {
            API.pool.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("pool_list").remove(data.id);
                    navigation.navigate("..");
                },
                function () {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            navigation.navigate("..");
        }
    };
};

export const pool_form_logic = new PoolFormLogic();
export const pool_form_routes = [
    new Route(/^\/environment\/(\d+)\/pool\/new$/, pool_form_logic.on_route_new, "pool"),
    new Route(/^\/environment\/(\d+)\/pool\/(\d+)$/, pool_form_logic.on_route_item, "pool"),
]