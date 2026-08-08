// ----------------------------------------------------------------------
// Pool logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "./rpc.js";
import { app_logic } from "./app_logic.js";
import { Tower } from "./lib.js";

export const pool_logic = {
    init: function () {
        $$("pool_form").bind($$("pool_list"));
    },

    can_run: function () {
        return app_logic.is_environment_selected();
    },

    show: function () {
        pool_logic.show_list();
    },

    show_list: function () {
        $$("pool_list_panel").show();
        pool_logic.load();
    },

    show_form: function () {
        $$("pool_form_panel").show();
    },

    // Load data info list
    load: function () {
        $$("pool_list").load("rpc->pool");
    },

    on_add: function () {
        $$("pool_form").clear();
        pool_logic.show_form();
    },

    on_save: function () {
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
                        pool_logic.show_list();
                        Tower.msg.complete("Created");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to create");
                    }
                );
            } else {
                data.environment_id = app_logic.current_env.id;
                API.pool.update_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        pool_logic.show_list();
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
        const data = $$("pool_list").getSelectedItem();
        $$("pool_form").setValues(data);
        pool_logic.show_form();
    },

    on_search: function (nv, ov) {
        console.log("Search", nv, ov);
    },

    on_delete: function () {
        const data = $$("pool_form").getValues();
        if (data.id) {
            API.pool.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("pool_list").remove(data.id);
                    pool_logic.show_list();
                },
                function () {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            pool_logic.show_list();
        }
    }
};
