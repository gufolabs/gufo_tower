var desktop_logic = {
    init: function() {
        environment_logic.init();
        datacenter_logic.init();
        pool_logic.init();
        node_logic.init();
        service_logic.init();
        settings_logic.init();
    },

    show: function() {
        $$("desktop").show();
        $$("sidebar").select("environment");
    },

    on_select_app: function(selection) {
        var logic = window[selection[0] + "_logic"];
        if(logic) {
            logic.show();
        }
    },

    select_environment: function(env) {
        $$("environment_label").setValue("NOC Tower: " + env.name);
    },

    on_menu_click: function(item_id) {
        switch(item_id) {
            case "logout":
                app_logic.logout();
                break;
            case "change_password":
                change_password_logic.show();
                break;
        }
    }
};
