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
        settings_logic.init();
        var env_id = app_logic.current_env.id;
        API.pull.is_pulled(env_id).then(
            function (result) {
                if (result) {
                    $$("service_list").clearAll();
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
                } else {
                    Tower.msg.failed("Repo is not pulled. Pull repo first");
                }
            }, function (err) {
                Tower.msg.failed("Cannot connect to server");
            }
        );
    },
    set_enabled: function (obj, common) {
        if (obj.hasOwnProperty('config') && obj['config'].hasOwnProperty('backup_power')) {
            return common.treecheckbox(obj, common) +
                common.space(obj, common) +
                '<span class="mywebix_badge">' +
                obj.config.power +
                "</span>" +
                '<span class="mywebix_badge" style="background-color: green !important;">' +
                obj.config.backup_power +
                "</span>"
        }
        else if (obj.hasOwnProperty('config') && obj['config'].hasOwnProperty('power')) {
            return common.treecheckbox(obj, common) +
                common.space(obj, common) +
                '<span class="mywebix_badge">' +
                obj.config.power +
                "</span>"
        }
        else {
            return common.treecheckbox(obj, common)
        }
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
        // we are filtering. staying on groupped service
        if (ids.length === 0) {
            return []
        }
        var data = $$("service_list").data.pull[ids[0].id];
        var form_info = $$("service_form").getValues();
        var form = $$("service_form");
        var ci, cv, fname;

        // possibly old service
        if (form_info[data.service] === undefined) {
            form = []
        }
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
                value: "Set that values to all nodes",
                type: "form",
                css: "greenbutton",
                width: 471,
                click: function (nv, ov) {
                    if (this.getFormView().getDirtyValues()) {
                        // Dynamically set tree data to leaves
                        var lines = [],
                            values = this.getFormView().getDirtyValues();
                        $$("service_list").data.each(function (v) {
                            if (v.$parent === ids[0].id) {
                                lines.push(v);
                            }
                        });
                        lines.forEach(function (line) {
                            // sorry for that.
                            for (var key in values) {
                                nm = key.split("-")[1];
                                val = values[key];
                                $$("service_list").data.pull[line.id].config[nm] = val;
                            }
                        });
                        $$("service_list").refresh();
                    }
                }
            });
            webix.ui(fm, form);
        }
        else {
            webix.ui(data.form, form);
        }

        cv = form.getChildViews();
        for (ci in cv) {
            fname = cv[ci]["data"].id;
            cv[ci].attachEvent(
                "onChange",
                (function (name) {
                    return function (nv, ov) {
                        if (this.validate()) {
                            // Dynamically set tree data
                            if (data.hasOwnProperty('config')) {
                                data.config[name] = nv;
                                $$("service_list").refresh();
                            }
                        }
                    }
                })(fname)
            );
            if (data.hasOwnProperty('config') && data.config[fname]) {
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
	sortGroupTitle:	function (){
        grid.markSorting("service", "asc");
        grid.sort(function(a,b){
        if (a.service === b.service)
            return (a.node>b.node)?1:-1;
        else
            return (a.service>b.service)?1:-1;
        });
    },
    on_group_table: function (mode) {
        if (mode === "init") {
            mode = $$("settings_form").getValues()["group_by"]
        }
        var grid = $$("service_list");
        grid.filter("");
        grid.ungroup();

        if (mode === "node") {
            grid.moveColumn("node", 0);
            grid.markSorting("service", "asc");
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
            grid.sort(function(a,b){
				if (a.node === b.node)
					return (a.service>b.service)?1:-1;
				else
					return (a.node>b.node)?1:-1;
			});
        } else if (mode === "service") {
            grid.moveColumn("service", 0);
            grid.markSorting("node", "asc");
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
            grid.sort(function(a,b){
				if (a.service === b.service)
					return (a.node>b.node)?1:-1;
				else
					return (a.service>b.service)?1:-1;
			});
        }
        var i = 0;
        grid.eachRow(function(id) {
            i++;
            if(i === 1) this.open(id);
        });
        grid.filterByAll();
    },
    on_expand_tree: function (mode) {
        if (mode)
            $$("service_list").openAll();
        else
            $$("service_list").closeAll();
    }
}
;

