// ----------------------------------------------------------------------
// Role logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "./rpc.js";
import { app_logic } from "./app_logic.js";
import { Tower } from "./lib.js";

export const role_logic = {
    init: function () {
    },

    can_run: function () {
        return app_logic.is_environment_selected();
    },

    show: function () {
        role_logic.show_list();
        $$("role_form").bind($$("role_list"));
    },

    show_list: function () {
        $$("role_list_panel").show();
        role_logic.load();
    },

    show_form: function () {
        $$("role_form_panel").show();
    },

    // Load data info list
    load: function () {
        $$("role_list").load("rpc->role");
    },

    on_add: function () {
        $$("role_form").clear();
        role_logic.show_form();
    },

    on_save: function () {
        var data,
            form = $$("role_form");

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
    },

    on_edit: function () {
        var data = $$("role_list").getSelectedItem();
        $$("role_form").setValues(data);
        role_logic.show_form();
    },

    on_search: function (nv, ov) {
        console.log("Search", nv, ov);
    },

    on_delete: function () {
        var data = $$("role_form").getValues();
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
    }
};
