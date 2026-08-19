// ----------------------------------------------------------------------
// Service Logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../rpc.js";
import { app_logic } from "../app/logic.js";
import { settings_logic } from "../settings/logic.js";
import { Tower } from "../lib.js";
import { Route } from "../route.js";

export class ServiceLogic {
    init = () => {
    };

    on_route = (env_id) => {
        return app_logic.with_environment(parseInt(env_id, 10)).then(() => {
            $$("service_panel").show();
            service_logic.load();
        });
    };

    load = () => {
        settings_logic.init();
        const env_id = app_logic.current_env.id;
        API.pull.is_pulled(env_id).then(
            function (result) {
                if (result) {
                    $$("service_list").clearAll();
                    API.service.get_service_list(env_id).then(
                        function (res) {
                            // Load service list
                            $$("service_list").parse(res);
                        },
                        function (err) {
                            Tower.msg.failed("Failed to get config");
                        }
                    );
                    API.service.get_forms(env_id).then(
                        function (res) {
                            // Load forms list
                            $$("service_form").parse(res);
                        },
                        function (err) {
                            Tower.msg.failed("Failed to get forms.");
                        }
                    );
                } else {
                    Tower.msg.failed("Repo is not pulled. Press Pull button on Environments tab");
                }
            }, function (err) {
                Tower.msg.failed("Cannot connect to server");
            }
        );
    };

    set_enabled = (obj, common) => {
        if (Object.hasOwn(obj, 'config') && Object.hasOwn(obj['config'], 'backup_power')) {
            return common.treecheckbox(obj, common) +
                common.space(obj, common) +
                '<span class="mywebix_badge">' +
                obj.config.power +
                "</span>" +
                '<span class="mywebix_badge" style="background-color: green !important;">' +
                obj.config.backup_power +
                "</span>"
        }
        else if (Object.hasOwn(obj, 'config') && Object.hasOwn(obj['config'], 'power')) {
            return common.treecheckbox(obj, common) +
                common.space(obj, common) +
                '<span class="mywebix_badge">' +
                obj.config.power +
                "</span>"
        }
        else {
            return common.treecheckbox(obj, common)
        }
    };

    on_column_group = (obj, common, name) => {
        const parent = obj.$parent ? obj.$parent.split("$")[1] : undefined;
        // let name = this.column;
        if (obj.$group && obj[name]) {
            // folder
            return common.space(obj, common) +
                common.icon(obj, common) +
                common.folder(obj, common) +
                "<span>" + obj[name] + "</span>"
        } else if (parent !== obj[name]) {
            return obj[name];
        } else {
            if (Object.hasOwn(obj, "node") &&
                Object.hasOwn(obj, "service") &&
                (obj.node === obj.service) &&
                (name === $$("service_list").Nk)) { // @todo: this code smells
                return obj[name];
            }
            return "";
        }
    };

    on_select_service = () => {
        const ids = $$("service_list").getSelectedId(true);
        // we are filtering. staying on groupped service
        if (ids.length === 0) {
            return;
        }
        const data = $$("service_list").data.pull[ids[0].id];
        const form_info = $$("service_form").getValues();
        let form = $$("service_form");
        let fname;

        // possibly old service
        if (form_info[data.service] === undefined) {
            form = []
        }
        data["form"] = form_info[data.service];
        // add button to propagate values to lower tree
        if (data.$level === 1) {
            const fm = data.form.map(function (e) {
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
                        const lines = [];
                        const values = this.getFormView().getDirtyValues();
                        $$("service_list").data.each(function (v) {
                            if (v.$parent === ids[0].id) {
                                lines.push(v);
                            }
                        });
                        lines.forEach(function (line) {
                            // sorry for that.
                            for (const key in values) {
                                const nm = key.split("-").pop();
                                const val = values[key];
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

        const cv = form.getChildViews();
        for (const ci in cv) {
            fname = cv[ci]["data"].id;
            cv[ci].attachEvent(
                "onChange",
                (function (name) {
                    return function (nv, ov) {
                        if (this.validate()) {
                            // Dynamically set tree data
                            if (Object.hasOwn(data, 'config')) {
                                data.config[name] = nv;
                                $$("service_list").refresh();
                            }
                        }
                    }
                })(fname)
            );
            if (Object.hasOwn(data, 'config') && data.config[fname]) {
                cv[ci].setValue(data.config[fname]);
            }
        }
    };

    on_save = () => {
        const r = [];
        const env_id = app_logic.current_env.id;
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
    };
    on_group_table = (mode) => {
        if (mode === "init") {
            mode = $$("settings_form").getValues()["group_by"]
        }
        const grid = $$("service_list");
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
            grid.sort(function (a, b) {
                if (a.node === b.node) {
                    return (a.service > b.service) ? 1 : -1;
                } else {
                    return (a.node > b.node) ? 1 : -1;
                }
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
            grid.sort(function (a, b) {
                if (a.service === b.service) {
                    return (a.node > b.node) ? 1 : -1;
                } else {
                    return (a.service > b.service) ? 1 : -1;
                }
            });
        }
        let i = 0;
        grid.eachRow(function (id) {
            i++;
            if (i === 1) {
                this.open(id);
            }
        });
        grid.filterByAll();
    };
    on_expand_tree = (mode) => {
        if (mode) {
            $$("service_list").openAll();
        } else {
            $$("service_list").closeAll();
        }
    };
};
export const service_logic = new ServiceLogic();
export const service_routes = [
    new Route(/^\/environment\/(\d+)\/service$/, service_logic.on_route, "service")
];