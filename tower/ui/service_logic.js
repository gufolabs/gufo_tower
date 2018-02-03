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

    on_column_group: function (obj, common, name) {
        var parent = obj.$parent ? obj.$parent.split("$")[1] : undefined;
        // var name = this.column;
        if (obj.$group && obj[name]) {
            return common.space(obj, common) +
                common.icon(obj, common) +
                common.folder(obj, common) +
                "<span>" + obj[name] + "</span>"
        } else if (parent !== obj[name]) {
            return obj[name];
        } else {
            return ""
        }
    },

    on_select_service: function () {
        var ids = $$("service_list").getSelectedId(true);
        var data = $$("service_list").data.pull[ids[0].id];
        var form_info = $$("service_form")._values;
        var form = $$("service_form");
        var cv, fname;
        if (form_info[data.service] === undefined) return [];
        data["form"] = form_info[data.service];
        // add button to propagate values to lower tree
        if (data.$level === 1) {
            var fm = data.form.map(function (e) {
                e.value = null;
                return e;
            });
            fm.unshift({
                view: "button",
                id: "my_button",
                value: "Set to all nodes",
                type: "form",
                inputWidth: 200,
                click: function (nv, ov) {
                    if (this.getFormView().validate()) {
                        // Dynamically set tree data to leaves
                        var lines = [];
                        $$("service_list").data.each(function (v) {
                            if (v.$parent === ids[0].id) {
                                lines.push(v);
                            }
                        });
                        lines.forEach(function (line) {
                            $$("service_list").data.pull[line.id].config[name] = nv;
                        });
                    }
                }
            });
            webix.ui(fm, form);
        }
        else {
            webix.ui(data.form, form);
        }

        cv = form.getChildViews();
        cv.forEach(function (ci) {
            fname = ci["data"].id;
            ci.attachEvent(
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
            if (data.hasOwnProperty('config') && data.config[fname]) {
                ci.setValue(data.config[fname]);
            }
        });
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

