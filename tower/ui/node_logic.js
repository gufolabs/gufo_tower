var node_logic = {
    init: function () {
        $$("node_form").bind($$("node_list"));
    },

    can_run: function () {
        return app_logic.is_environment_selected();
    },

    show: function () {
        node_logic.show_list();
    },

    show_list: function () {
        $$("node_list_panel").show();
        node_logic.load();
    },

    show_form: function () {
        $$("node_form_panel").show();
    },

    // Load data info list
    load: function () {
        $$("node_list").load("rpc->node");
    },

    on_add: function () {
        var i = $$("datacenter_list").data.pull;
        var d = $$("node_form").elements.datacenter;
        var my_keys = Object.keys(i);
        for (j = 0; j < my_keys.length; j++) {
            if (my_keys[j] != 'id') {
                var obj = i[my_keys[j]];
                d.data.options.add({id: obj.id, value: obj.name});
            }
        }

        node_logic.show_form();
        $$("node_form").setValues({
            login_as: "ansible",
            node_type: 3,
            is_enabled: true
        });
    },

    on_save: function () {
        var data,
            form = $$("node_form");

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
                        Tower.msg.failed("Failed to change "+ err);
                    }
                );
            }
        } else {
            Tower.msg.failed("Error in data");
        }
    },

    on_edit: function () {
        var data = $$("node_list").getSelectedItem();
        $$("node_form").setValues(data);
        node_logic.show_form();
    },

    on_search: function (nv, ov) {
        console.log("Search", nv, ov);
    },

    on_delete: function () {
        var data = $$("node_form").getValues();
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
    }
};
