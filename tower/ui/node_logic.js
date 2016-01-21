var node_logic = {
    init: function() {
        $$("node_form").bind($$("node_list"));
    },

    show: function() {
        node_logic.show_list();
    },

    show_list: function() {
        $$("node_list_panel").show();
        node_logic.load();
    },

    show_form: function() {
        $$("node_form_panel").show();
    },

    // Load data info list
    load: function() {
        $$("node_list").load("rpc->node");
    },

    on_add: function() {
        $$("node_form").clear();
        node_logic.show_form();
    },

    on_save: function() {
        var data,
            form = $$("node_form");

        if (form.validate()) {
            data = form.getValues();
            data.environment = app_logic.current_env.id;
            if(data.id === undefined) {
                API.node.create_item(data).then(
                    function(result) {
                        form.setValues(result);
                        form.save();
                        node_logic.show_list();
                        Tower.msg.complete("Created");
                    },
                    function(err) {
                        Tower.msg.failed("Failed to create");
                    }
                );
            } else {
                API.node.update_item(data).then(
                    function(result) {
                        form.setValues(result);
                        form.save();
                        node_logic.show_list();
                        Tower.msg.complete("Changed");
                    },
                    function(err) {
                        Tower.msg.failed("Failed to change");
                    }
                );
            }
        } else {
            Tower.msg.failed("Error in data");
        }
    },

    on_select: function() {
        var data = $$("node_list").getSelectedItem();
        app_logic.select_node(data.name);
    },

    on_edit: function() {
        var data = $$("node_list").getSelectedItem();
        $$("node_form").setValues(data);
        node_logic.show_form();
    },

    on_search: function(nv, ov) {
        console.log("Search", nv, ov);
    },
    
    on_delete: function() {
        var data = $$("node_form").getValues();
        if(data.id) {
            API.node.delete_item(data).then(
                function() {
                    Tower.msg.complete("Deleted");
                    $$("node_list").remove(data.id);
                    node_logic.show_list();
                },
                function() {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            node_logic.show_list();
        }
    }
};
