export const node_logic = {
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
        var dc = $$("node_form").elements.datacenter;
        var nt = $$("node_form").elements.node_type;

        API.datacenter.get_items().then(result => {
            if (dc.data.options.count() == 0)
                result.data.forEach(el => dc.data.options.add({ id: el.id, value: el.name }))
        }).then(
            API.nodetype.get_items().then(result => {
                if (nt.data.options.count() == 0)
                    result.data.forEach(el => nt.data.options.add({ id: el.id, value: el.name }))
            })
        ).then(function () {
            node_logic.show_form();
            $$("node_form").setValues({
                login_as: "ansible",
                node_type: 1,
                is_enabled: true
            });
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
                        Tower.msg.failed("Failed to change " + err);
                    }
                );
            }
        } else {
            Tower.msg.failed("Error in data");
        }
    },

    on_edit: function () {
        var data = $$("node_list").getSelectedItem();
        data.datacenter = data.datacenter.id;
        data.node_type = data.node_type.id;
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
