var environment_logic = {
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
    load: function() {
        $$("environment_list").load("rpc->environment");
    },

    on_add: function() {
        $$("environment_form").clear();
        environment_logic.show_form();
    },

    on_save: function () {
        var data,
            form = $$("environment_form");

        if (form.validate()) {
            data = form.getValues();
            if(data.id === undefined) {
                API.environment.create_item(data).then(
                    function(result) {
                        form.setValues(result);
                        form.save();
                        environment_logic.show_list();
                        Tower.msg.complete("Created");
                    },
                    function(err) {
                        Tower.msg.failed("Failed to create");
                    }
                );
            } else {
                API.environment.update_item(data).then(
                    function(result) {
                        form.setValues(result);
                        form.save();
                        environment_logic.show_list();
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

    on_select: function () {
        var data = $$("environment_list").getSelectedItem();
        app_logic.select_environment(data);
        $$("environment_inventory_button").enable();
        $$("environment_pull_button").enable();
        $$("environment_deploy_button").enable();
    },

    on_edit: function () {
        var data = $$("environment_list").getSelectedItem();
        $$("environment_form").setValues(data);
        environment_logic.show_form();
    },

    on_search: function (nv, ov) {
        console.log("Search", nv, ov);
    },

    on_delete: function() {
        var data = $$("environment_form").getValues();
        if(data.id) {
            API.environment.delete_item(data).then(
                function() {
                    Tower.msg.complete("Deleted");
                    $$("environment_list").remove(data.id);
                    // @todo: Unselect environment
                    environment_logic.show_list();
                },
                function() {
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
                text: JSON.stringify(result, undefined, 2)
            });
            $$("environment_inventory_panel").show();
        }, function (err) {
            Tower.msg.failed("Cannot get inventory");
        });
    },

    on_pull: function () {
        var env_id = app_logic.current_env.id,
            check_status = function (env_id, job_id) {
                API.pull.get_job_status(env_id, job_id).then(
                    function (result) {
                        if (result.complete) {
                            // Pull done
                            if (result.status) {
                                Tower.msg.complete("Pull complete");
                            } else {
                                Tower.msg.failed("Failed to pull");
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
        var env_id = app_logic.current_env.id,
            env_name = app_logic.current_env.name,
            rx_progress = /^(ok|changed|unreachable|failed|fatal): \[/mg,
            rx_task = /^.+?\*{5}\s*$/mg,
            rx_line = /^(ok|changed|unreachable|failed|fatal|skipping): \[.+?$/mg,
            deploy = function () {
                var xhr = new XMLHttpRequest(),
                    offset = 0,
                    output_panel = $$("environment_deploy_output"),
                    badges_panel = $$("environment_deploy_badges"),
                    clock = $$("environment_deploy_clock"),
                    output = "",
                    start_time = Date.now(),
                    running=true,
                    status = {
                        ok: 0,
                        changed: 0,
                        unreach: 0,
                        failed: 0,
                        status: "<i class='fa fa-cog fa-spin'></i> Running"
                    },
                    //
                    // Update wall clocks
                    //
                    update_clock = function() {
                        var dt = Math.floor((Date.now() - start_time) / 1000),
                            s = dt % 60,  // Seconds
                            m = Math.floor((dt - s) / 60),
                            t; // Minutes
                        s = (s >= 10) ? ("" + s) : ("0" + s);
                        m = (m >= 10) ? ("" + m) : ("0" + m);
                        t = m + ":" + s;
                        clock.setValues({time: t});
                        if(running) {
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
                    "/deploy/" + env_name + "/",
                    true
                );
                xhr.onprogress = function () {
                    var ft = xhr.responseText,
                        match, t, ct;
                    // Process only last chunk
                    t = webix.template.escape(ft.substr(offset));
                    offset = ft.length;
                    // Get progress
                    while (match = rx_progress.exec(t)) {
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
                    // Update deploy log
                    ct = t.replace(rx_task, function (x) {
                        return "<span class='ansible-task'>" + x + "</span>";
                    });
                    ct = ct.replace(rx_line, function (x) {
                        var c = x.split(":")[0];
                        if (c === "fatal") {
                            c = "failed";
                        }
                        return "<span class='ansible-" + c + "'>" + x + "</span>";
                    });
                    output += ct;
                    output_panel.setHTML(output);
                    output_panel.scrollTo(0, 100000);
                    // Update badges
                    badges_panel.setValues(status);
                };
                xhr.onload = function () {
                    if (status.unreach || status.failed) {
                        status.status = "<i class='fa fa-bolt'></i> Failed";
                        Tower.msg.failed("Deploy failed");
                        running = false;  // Stop clock
                    } else {
                        status.status = "<i class='fa fa-check-circle'></i> Complete";
                        Tower.msg.complete("Deploy completed");
                        running = false;  // Stop clock
                    }
                    badges_panel.setValues(status);
                };
                xhr.onerror = function () {
                    badges_panel.setValues(status);
                    status.status = "<i class='fa fa-bolt'></i> Failed";
                    Tower.msg.failed("Deploy failed");
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
                    Tower.msg.failed("Repo is not pulled. Pull repo first");
                }
            }, function (err) {
                Tower.msg.failed("Cannot connect to server");
            });
    }
};
