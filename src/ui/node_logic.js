// ----------------------------------------------------------------------
// Node logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "./rpc.js";
import { app_logic } from "./app_logic.js";
import { Tower } from "./lib.js";

export class NodeLogic {
    init = () => {
        $$("node_form").bind($$("node_list"));
    };

    can_run = () => {
        return app_logic.is_environment_selected();
    };

    show = () => {
        node_logic.show_list();
    };

    show_list = () => {
        $$("node_list_panel").show();
        node_logic.load();
    };

    show_form = () => {
        $$("node_form_panel").show();
    };

    // Load data info list
    load = () => {
        $$("node_list").load("rpc->node");
    };

    on_add = () => {
        const dc = $$("node_form").elements.datacenter;
        const nt = $$("node_form").elements.node_type;

        API.datacenter.get_items().then(result => {
            if (dc.data.options.count() === 0) {
                result.data.forEach(el => dc.data.options.add({ id: el.id, value: el.name }))
            }
        }).then(
            API.nodetype.get_items().then(result => {
                if (nt.data.options.count() === 0) {
                    result.data.forEach(el => nt.data.options.add({ id: el.id, value: el.name }))
                }
            })
        ).then(function () {
            node_logic.show_form();
            $$("node_form").setValues({
                login_as: "ansible",
                node_type: 1,
                is_enabled: true
            });
        });

    };

    on_save = () => {
        let data;
        const form = $$("node_form");

        if (form.validate()) {
            data = form.getValues();
            data.environment = app_logic.current_env.id;
            if (data.id === undefined) {
                API.node.create_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        node_logic.show_list();
                        Tower.msg.complete("Created");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to create " + err);
                    }
                );
            } else {
                API.node.update_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        node_logic.show_list();
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
    };

    on_edit = () => {
        const data = $$("node_list").getSelectedItem();
        data.datacenter = data.datacenter.id;
        data.node_type = data.node_type.id;
        $$("node_form").setValues(data);
        node_logic.show_form();
    };

    on_search = (nv, ov) => {
        console.log("Search", nv, ov);
    };

    on_delete = () => {
        const data = $$("node_form").getValues();
        if (data.id) {
            API.node.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("node_list").remove(data.id);
                    node_logic.show_list();
                },
                function () {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            node_logic.show_list();
        }
    };
};
export const node_logic = new NodeLogic();