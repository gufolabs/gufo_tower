// ----------------------------------------------------------------------
// Role logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "./rpc.js";
import { app_logic } from "./app_logic.js";
import { Tower } from "./lib.js";

export class RoleLogic {
    init = () => {
    };

    can_run = () => {
        return app_logic.is_environment_selected();
    };

    show = () => {
        role_logic.show_list();
        $$("role_form").bind($$("role_list"));
    };

    show_list = () => {
        $$("role_list_panel").show();
        role_logic.load();
    };

    show_form = () => {
        $$("role_form_panel").show();
    };

    // Load data info list
    load = () => {
        $$("role_list").load("rpc->role");
    };

    on_add = () => {
        $$("role_form").clear();
        role_logic.show_form();
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
                        role_logic.show_list();
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
                        role_logic.show_list();
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

    on_edit = () => {
        const data = $$("role_list").getSelectedItem();
        $$("role_form").setValues(data);
        role_logic.show_form();
    };

    on_search = (nv, ov) => {
        console.log("Search", nv, ov);
    };

    on_delete = () => {
        const data = $$("role_form").getValues();
        if (data.id) {
            API.role.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("role_list").remove(data.id);
                    role_logic.show_list();
                },
                function () {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            role_logic.show_list();
        }
    };
};

export const role_logic = new RoleLogic();