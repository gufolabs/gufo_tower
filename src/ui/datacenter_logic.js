// ----------------------------------------------------------------------
// Datacenter logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "./rpc.js";
import { Tower } from "./lib.js";

export const datacenter_logic = {
    init: function () {
    },

    show: function () {
        datacenter_logic.show_list();
        $$("datacenter_form").bind($$("datacenter_list"));
    },

    show_list: function () {
        $$("datacenter_list_panel").show();
        datacenter_logic.load();
    },

    show_form: function () {
        $$("datacenter_form_panel").show();
    },

    // Load data info list
    load: function () {
        $$("datacenter_list").load("rpc->datacenter");
    },

    on_add: function () {
        $$("datacenter_form").clear();
        datacenter_logic.show_form();
    },

    on_save: function () {
        let data,
            form = $$("datacenter_form");

        if (form.validate()) {
            data = form.getValues();
            if (data.id === undefined) {
                API.datacenter.create_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        datacenter_logic.show_list();
                        Tower.msg.complete("Created");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to create " + err);
                    }
                );
            } else {
                API.datacenter.update_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        datacenter_logic.show_list();
                        Tower.msg.complete("Changed");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to change " + err);
                    }
                );
            }
        } else {
            Tower.msg.failed("Error in data");
        }
    },

    on_edit: function () {
        let data = $$("datacenter_list").getSelectedItem();
        $$("datacenter_form").setValues(data);
        datacenter_logic.show_form();
    },

    on_search: function (nv, ov) {
        console.log("Search", nv, ov);
    },

    on_delete: function () {
        let data = $$("datacenter_form").getValues();
        if (data.id) {
            API.datacenter.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("datacenter_list").remove(data.id);
                    datacenter_logic.show_list();
                },
                function () {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            datacenter_logic.show_list();
        }
    }
};
