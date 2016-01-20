var datacenter_logic = {
    init: function() {},

    show: function() {
        datacenter_logic.show_list();
        $$("datacenter_form").bind($$("datacenter_list"));
    },

    show_list: function() {
        $$("datacenter_list_panel").show();
    },

    show_form: function() {
        $$("datacenter_form_panel").show();
    },

    on_save: function() {
        var data,
            form = $$("datacenter_form");

        if (form.validate()) {
            data = form.getValues();
            if(data.id === undefined) {
                API.datacenter.create_item(data).then(
                    function(result) {
                        form.save();
                        datacenter_logic.show_list();
                        Tower.msg.complete("Created");
                    },
                    function(err) {
                        Tower.msg.failed("Failed to create");
                    }
                );
            } else {
                API.datacenter.update_item(data).then(
                    function(result) {
                        form.save();
                        datacenter_logic.show_list();
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
        var data = $$("datacenter_list").getSelectedItem();
        $$("datacenter_form").setValues(data);
        datacenter_logic.show_form();
    },

    on_search: function(nv, ov) {
        console.log("Search", nv, ov);
    }
};
