// ----------------------------------------------------------------------
// Environment logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "./rpc.js";
import { app_logic } from "./app_logic.js";
import { Tower } from "./lib.js";

export const environment_logic = {
    PULL_CHECK_INTERVAL: 1000,

    init: function () {
        webix.extend($$("environment_list"), webix.ProgressBar);
        $$("environment_form").bind($$("environment_list"));
    },

    show: function () {
        environment_logic.show_list();
        //self.load();
    },

    show_list: function () {
        $$("environment_list_panel").show();
        environment_logic.load();
    },

    show_form: function () {
        $$("environment_form_panel").show();
    },

    // Load data info list
    load: function () {
        $$("environment_list").load("rpc->environment");
    },

    on_add: function () {
        environment_logic.show_form();
        $$("environment_form").setValues({
            env_type: "eval",
            install_method: "git",
            playbook_link: "git+https://github.com/gufolabs/noc@stable",
            installation_name: "Unconfigured installation",
            config_order: "yaml:///opt/noc/etc/tower.yml,yaml:///opt/noc/etc/settings.yml,env:///NOC",
            name: "NOC"
        });
        $$("pulled_label").setHTML("");
    },

    on_save: function () {
        let data;
        const form = $$("environment_form");

        if (form.validate()) {
            data = form.getValues();
            if (data.id === undefined) {
                API.environment.create_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        environment_logic.show_list();
                        Tower.msg.complete("Created");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to create " + err);
                    }
                );
            } else {
                API.environment.update_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        environment_logic.show_list();
                        Tower.msg.complete("Changed");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to change" + err);
                    }
                );
            }
        } else {
            Tower.msg.failed("Error in data");
        }
    },

    on_select: function () {
        const data = $$("environment_list").getSelectedItem();
        app_logic.select_environment(data);
        $$("environment_inventory_button").enable();
        $$("environment_pull_button").enable();
        $$("environment_deploy_button").enable();
        $$("deployment_options").enable();
    },

    on_edit: function () {
        const data = $$("environment_list").getSelectedItem();
        $$("environment_form").setValues(data);
        API.pull.is_pulled(data.id).then(
            function (result) {
                if (result) {
                    $$("pulled_label").setHTML("<span style='color: red; font-weight: bold;'>Playbook Repo is pulled, now you can only change branch, not URL. To change URL you have to manually remove playbook dir from %TOWER%/var/tower/playbooks/%Env name%</span>");
                } else {
                    $$("pulled_label").setHTML("");
                }
            }, function (err) {
                Tower.msg.failed("Cannot connect to server");
            }
        );
        environment_logic.show_form();
    },

    on_search: function (nv, ov) {
        console.log("Search", nv, ov);
    },

    on_delete: function () {
        const data = $$("environment_form").getValues();
        if (data.id) {
            API.environment.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("environment_list").remove(data.id);
                    // @todo: Unselect environment
                    environment_logic.show_list();
                },
                function () {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            environment_logic.show_list();
        }
    },

    on_show_inventory: function () {
        API.environment.ansible_inventory(app_logic.current_env.id).then(function (result) {
            $$("environment_inventory_text").setValues({
                text: result  // JSON.stringify(result, undefined, 2)
            });
            $$("environment_inventory_panel").show();
        }, function (err) {
            Tower.msg.failed("Cannot get inventory");
        });
    },

    on_pull: function () {
        const env_id = app_logic.current_env.id;
        const check_status = function (env_id, job_id) {
            API.pull.get_job_status(env_id, job_id).then(
                function (result) {
                    if (result.complete) {
                        // Pull done
                        if (result.status) {
                            Tower.msg.complete("Pull complete");
                            Tower.notification("Pull complete");
                        } else {
                            Tower.msg.failed("Failed to pull");
                            Tower.notification("Failed to pull");
                        }
                        $$("environment_list").hideProgress();
                    } else {
                        // Run another check
                        webix.delay(check_status, environment_logic,
                            [env_id, job_id],
                            environment_logic.PULL_CHECK_INTERVAL);
                    }
                },
                function (err) {
                    Tower.msg.failed("Failed to pull");
                    Tower.notification("Failed to pull");
                    $$("environment_list").hideProgress();
                }
            );
        };

        $$("environment_list").showProgress({
            type: "icon"
        });
        Tower.msg.started("Start pulling");
        API.pull.start_job(env_id).then(
            function (result) {
                webix.delay(check_status, environment_logic,
                    [env_id, result.job],
                    environment_logic.PULL_CHECK_INTERVAL);
            },
            function (err) {
                $$("environment_list").hideProgress();
                Tower.msg.failed("Cannot pull repo");
            }
        );
    },

    on_deploy: function () {
        const env_id = app_logic.current_env.id;
        const env_name = app_logic.current_env.name;
        const rx_progress = /^(ok|changed|unreachable|failed|fatal): \[/mg;
        const rx_task = /^.+?\*{3}\s*$/mg;
        const rx_line = /^(ok|changed|unreachable|failed|fatal|skipping): \[.+?$/mg;
        const rx_stars = /\s+\*{3,}/;
        const deploy = function () {
            const xhr = new XMLHttpRequest();
            let offset = 0,
                output = "",
                running = true;
            const output_panel = $$("environment_deploy_output");
            const badges_panel = $$("environment_deploy_badges");
            const clock = $$("environment_deploy_clock");
            const start_time = Date.now();
            const status = {
                ok: 0,
                changed: 0,
                unreach: 0,
                failed: 0,
                status: "<i class='fa fa-cog fa-spin'></i> Running"
            };
            //
            // Update wall clocks
            //
            const update_clock = function () {
                const dt = Math.floor((Date.now() - start_time) / 1000);
                let s = dt % 60,  // Seconds
                    m = Math.floor((dt - s) / 60); // Minutes                        
                s = (s >= 10) ? ("" + s) : ("0" + s);
                m = (m >= 10) ? ("" + m) : ("0" + m);
                const t = m + ":" + s;
                clock.setValues({ time: t });
                if (running) {
                    webix.delay(update_clock, output_panel, [], 1000);
                }
            };
            // Reset badges
            badges_panel.setValues(status);
            // Switch to deploy panel
            $$("environment_deploy_panel").show();
            Tower.msg.started("Deploying " + env_name);
            // Run streaming http request
            output_panel.setHTML("");  // Clean output
            xhr.open(
                "GET",
                "/deploy/" + env_id + "/?deployment_options=" + $$("deployment_options").getValue(),
                true
            );
            xhr.onprogress = function () {
                const ft = xhr.responseText;
                let match, ct;
                // Process only last chunk
                const t = webix.template.escape(ft.substr(offset));
                offset = ft.length;
                // Get progress
                while ((match = rx_progress.exec(t))) {
                    switch (match[1]) {
                        case "ok":
                            status.ok++;
                            break;
                        case "changed":
                            status.changed++;
                            break;
                        case "unreachable":
                            status.unreach++;
                            break;
                        case "failed":
                        case "fatal":
                            status.failed++;
                            break;
                    }
                }
                if (t.match(/(\.\.\.ignoring)/)) {
                    if (status.failed > 0) {
                        status.failed--;
                    }
                }
                // Update deploy log
                ct = t.replace(rx_task, function (x) {
                    x = x.replace(rx_stars, "");
                    return "<span class='ansible-task' style=white-space:nowrap>" + x + "<span style='float: right'>" + clock.getValues().time + "</span></span>";
                });
                ct = ct.replace(rx_line, function (x) {
                    let c = x.split(":")[0];
                    if (c === "fatal") {
                        c = "failed";
                    }
                    return "<span class='ansible-" + c + "'>" + x + "</span>";
                });
                output += ct;
                output_panel.setHTML(output);
                output_panel.scrollTo(0, 10000000);
                // Update badges
                badges_panel.setValues(status);
            };
            xhr.onload = function () {
                if (status.unreach || status.failed) {
                    status.status = "<i class='fa fa-bolt'></i> Failed";
                    Tower.msg.failed("Deploy failed");
                    Tower.notification("Deploy failed");
                    running = false;  // Stop clock
                } else {
                    status.status = "<i class='fa fa-check-circle'></i> Complete";
                    Tower.msg.complete("Deploy completed");
                    Tower.notification("Deploy completed");
                    running = false;  // Stop clock
                }
                badges_panel.setValues(status);
            };
            xhr.onerror = function () {
                badges_panel.setValues(status);
                status.status = "<i class='fa fa-bolt'></i> Failed";
                Tower.msg.failed("Deploy failed");
                Tower.notification("Deploy failed");
                running = false;  // Stop clock
            };
            xhr.send();
            update_clock();
        };

        API.pull.is_pulled(env_id).then(
            function (result) {
                if (result) {
                    deploy();
                } else {
                    Tower.msg.failed("Repo is not pulled. Press Pull button on Environments tab");
                }
            }, function (err) {
                Tower.msg.failed("Cannot connect to server");
            }
        );
    }
};
