// ----------------------------------------------------------------------
// Environment deploy logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { app_logic } from "../../app/logic.js";
import { Tower } from "../../lib.js";
import { Route } from "../../route.js";

export class EnvironmentDeployLogic {
    init = () => {
    };

    on_route = (e_id) => {
        const env_id = parseInt(e_id, 10);
        return app_logic.with_environment(env_id).then(() => {
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
                    `/deploy/${env_id}/?deployment_options=${$$("deployment_options").getValue()}`,
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
                            default:
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

            return API.pull.is_pulled(env_id)
                .then((result) => {
                    if (result) {
                        deploy();
                    } else {
                        Tower.msg.failed(
                            "Repo is not pulled. Press Pull button on Environments tab"
                        );
                    }
                })
                .catch(() => {
                    Tower.msg.failed("Cannot connect to server");
                });
        });
    };
};

export const environment_deploy_logic = new EnvironmentDeployLogic();

export const environment_deploy_routes = [
    new Route(/^\/environment\/(\d+)\/deploy$/, environment_deploy_logic.on_route, "environment"),
];