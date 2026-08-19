// ----------------------------------------------------------------------
// Role Form logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { app_logic } from "../../app/logic.js";
import { Tower } from "../../lib.js";
import { Route } from "../../route.js";

export class RoleFormLogic {
    init = () => {
    };

    on_route_new = (env_id) => {
        return app_logic.with_environment(parseInt(env_id, 10)).then(() => {
            $$("role_form").clear();
            $$("role_form_panel").show();
        });
    };

    on_route_item = (env_id, role_id) => {
        return app_logic.with_environment(parseInt(env_id, 10))
            .then(() => API.role.get_item({ id: parseInt(role_id, 10) }))
            .then((data) => {
                $$("role_form").setValues(data);
                $$("role_form_panel").show();
            })
            .catch((err) => {
                Tower.msg.failed("Failed to get data");
            }
            );
    };

    on_save = () => {
        let data;
        const form = $$("role_form");

        if (form.validate()) {
            data = form.getValues();
            data.environment = app_logic.current_env.id;
            if (data.id === undefined) {
                API.role.create_item(data).then(
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
                API.role.update_item(data).then(
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
        const data = $$("role_form").getValues();
        if (data.id) {
            API.role.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("role_list").remove(data.id);
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

export const role_form_logic = new RoleFormLogic();
export const role_form_routes = [
    new Route(/^\/environment\/(\d+)\/role\/new$/, role_form_logic.on_route_new, "role"),
    new Route(/^\/environment\/(\d+)\/role\/(\d+)$/, role_form_logic.on_route_item, "role"),
]