var pool_logic = {
    init: function() {
        $$("pool_form").bind($$("pool_list"));
    },

    show: function() {
        pool_logic.show_list();
    },

    show_list: function() {
        $$("pool_list_panel").show();
    },

    show_form: function() {
        $$("pool_form_panel").show();
    },

    on_save: function() {
        var data,
            form = $$("pool_form");

        if (form.validate()) {
            data = form.getValues();
            data.environment = app_logic.current_env.id;
            if(data.id === undefined) {
                API.pool.create_item(data).then(
                    function(result) {
                        form.save();
                        pool_logic.show_list();
                        Tower.msg.complete("Created");
                    },
                    function(err) {
                        Tower.msg.failed("Failed to create");
                    }
                );
            } else {
                API.pool.update_item(data).then(
                    function(result) {
                        form.save();
                        pool_logic.show_list();
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

    on_edit: function() {
        var data = $$("pool_list").getSelectedItem();
        $$("pool_form").setValues(data);
        pool_logic.show_form();
    },

    on_search: function(nv, ov) {
        console.log("Search", nv, ov);
    }
};
