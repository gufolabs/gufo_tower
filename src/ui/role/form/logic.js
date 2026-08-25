// ----------------------------------------------------------------------
// Role Form logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route, router } from "../../route.js";
import { current_env } from "../../state.js";

export class RoleFormLogic {
    on_route_new = async (env_id) => {
        await current_env.with(parseInt(env_id, 10));
        $$("role_form").clear();
        $$("role_form_panel").show();
    };

    on_route_item = async (env_id, role_id) => {
        try {
            await current_env.with(parseInt(env_id, 10));
            const data = await API.role.get_item({
                id: parseInt(role_id, 10)
            });
            $$("role_form").setValues(data);
            $$("role_form_panel").show();
        } catch {
            Tower.msg.failed("Failed to get data");
        }
    };
    to_list = () => {
        navigation.navigate(`/environment/${current_env.state.id}/role`);
    }

    on_save = async () => {
        const form = $$("role_form");
        if (!form.validate()) {
            Tower.msg.failed("Error in data");
            return;
        }
        const data = form.getValues();
        data.environment = current_env.state.id;
        try {
            if (data.id === undefined) {
                await API.role.create_item(data);
                this.to_list();
                Tower.msg.complete("Created");
            } else {
                await API.role.update_item(data);
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
        const data = $$("role_form").getValues();

        if (data.id) {
            try {
                await API.role.delete_item(data);
                Tower.msg.complete("Deleted");
                $$("role_list").remove(data.id);
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

export const role_form_logic = new RoleFormLogic();
router.push(
    new Route(/^\/environment\/(\d+)\/role\/new$/, role_form_logic.on_route_new, "role"),
    new Route(/^\/environment\/(\d+)\/role\/(\d+)$/, role_form_logic.on_route_item, "role")
);