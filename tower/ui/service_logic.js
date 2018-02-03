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
        API.service.get_service_list(env_id).then(
            function (result) {
                // Load service list
                $$("service_list").parse(result);
            },
            function (err) {
                Tower.msg.failed("Failed to get config");
            }
        );
        API.service.get_forms(env_id).then(
            function (result) {
                // Load forms list
                $$("service_form").parse(result);
            },
            function (err) {
                Tower.msg.failed("Failed to get forms.");
            }
        );

    },

    on_column_group: function (obj, common) {
        var parent = obj.$parent ? obj.$parent.split("$")[1] : undefined;
        var name = this.column;
        if(obj.$group && obj[name]) {
            return common.space(obj, common) +
                common.icon(obj, common) +
                common.treecheckbox(obj, common) +
                common.folder(obj, common) +
                "<span>" + obj[name] + "</span>"
        } else if(parent !== obj[name]) {
            return obj[name];
        } else {
            return ""
        }
    },
    node_template: function (obj, common) {
        this.on_column_group(obj, common, "node")
    },

    service_template: function (obj, common) {
        this.on_column_group(obj, common, "service")
    },
    on_select_service: function () {
        var ids = $$("service_list").getSelectedId(true);
        var data = $$("service_list").data.pull[ids[0].id];
        var form_info = $$("service_form")._values;
        var form = $$("service_form")
        var ci, cv, fname;
        if (form_info[data.service] === undefined) return []
        data["form"] = form_info[data.service];
        webix.ui(data.form, form);
        cv = form.getChildViews();
        for (ci in cv) {
            fname = cv[ci]["data"].id;
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
            if (!v.config) {
                return;
            }
            r.push({
                config: v.config,
                present: v.checked,
                id: v.id
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
    },
    on_group_table: function (mode) {
        if (mode == null) {
            mode = "service"
        }
        var grid = $$("service_list");
        grid.filter("");
        grid.ungroup();

        if (mode === "node") {
            grid.moveColumn("node", 0);
            grid.sort({
                by: "node",
                dir: "asc"
            });
            grid.group({
                by: "node",
                map: {
                    node: [
                        function (obj) {
                            return obj.node
                        }
                    ]
                }
            });
        } else if (mode === "service") {
            grid.moveColumn("service", 0);
            grid.sort({
                by: "service",
                dir: "asc"
            });
            grid.group({
                by: "service",
                map: {
                    service: [
                        function (obj) {
                            return obj.service
                        }
                    ]
                }
            });
        }
        grid.filterByAll();
    },
    on_expand_tree: function (mode) {
        if (mode)
            $$("service_list").openAll();
        else
            $$("service_list").closeAll();
    }
};

