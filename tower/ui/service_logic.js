var service_logic = {
    init: function () {
    },

    can_run: function () {
        return app_logic.is_environment_selected();
    },

    show: function () {
        $$("service_panel").show();
        service_logic.load();
    },

    load: function () {
        var env_id = app_logic.current_env.id;
        API.service.get_config(env_id).then(
            function (result) {
                // Load service list
                $$("service_list").parse(result);
            },
            function (err) {
                Tower.msg.failed("Failed to get config");
            }
        );
    },

    on_select_service: function (ids) {
        var data = $$("service_list").getItem(ids[0]),
            nodes_list = $$("service_nodes_list"),
            form = $$("service_form"),
            ci, cv, fname;
        // Nodes list
        nodes_list.clearAll();
        nodes_list.parse(data.nodes);
        // Set up form
        webix.ui(data.form, form);
        cv = form.getChildViews();
        for (ci in cv) {
            fname = cv[ci].config.id;
            cv[ci].attachEvent(
                "onChange",
                (function (name) {
                    return function (nv, ov) {
                        if (this.validate()) {
                            // Dynamically set tree data
                            data.config[name] = nv;
                        }
                    }
                })(fname)
            );
            if (data.config[fname]) {
                cv[ci].setValue(data.config[fname]);
            }
        }
    },

    on_save: function () {
        var r = [],
            env_id = app_logic.current_env.id;
        $$("service_list").data.each(function (v) {
            if (!v.nodes) {
                return;
            }
            r.push({
                service: v.service,
                pool: v.pool,
                nodes: v.nodes,
                config: v.config
            });
        });
        API.service.save_config(env_id, r).then(
            function (result) {
                Tower.msg.complete("Config saved");
            },
            function (error) {
                Tower.msg.failed("Failed to save");
            }
        );
    }
};
