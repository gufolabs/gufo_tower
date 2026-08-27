// ----------------------------------------------------------------------
// Environment deploy logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route, router } from "../../route.js";
import { environment_deploy_form } from "./form/ui.js";
import { on_deploy, current_env, deploy_options } from "../../state.js";

export class EnvironmentDeployLogic {
    form = webix.ui(environment_deploy_form);

    rx_progress = /^(ok|changed|unreachable|failed|fatal): \[/mg;
    rx_task = /^.+?\*{3}\s*$/mg;
    rx_line = /^(ok|changed|unreachable|failed|fatal|skipping): \[.+?$/mg;
    rx_stars = /\s+\*{3,}/;

    init = () => {
        console.log("init");
        on_deploy.subscribe(() => {
            console.log("received");
            this.on_deploy();
        });
    };

    on_route = (e_id) => {
        const env_id = parseInt(e_id, 10);
        return current_env.with(env_id).then(() => {
            $$("environment_deploy_panel").show();
            this.form.show();
        });
    };

    on_deploy = () => {
        const env = current_env.state;
        return API.pull.is_pulled(env.id)
            .then((result) => {
                if (!result) {
                    Tower.msg.failed(
                        "Repo is not pulled. Press Pull button on Environments tab"
                    );
                    return;
                }

                this.run_deploy(env);
            })
            .catch(() => {
                Tower.msg.failed("Cannot connect to server");
            });
    };

    run_deploy = (env) => {
        const output_panel = $$("environment_deploy_output");
        const badges_panel = $$("environment_deploy_badges");
        const clock = $$("environment_deploy_clock");
        const status = {
            ok: 0,
            changed: 0,
            unreach: 0,
            failed: 0,
            status: "<i class='fa fa-cog fa-spin'></i> Running"
        };
        let offset = 0;
        let output = "";
        let running = true;
        const start_time = Date.now();
        badges_panel.setValues(status);
        output_panel.setHTML("");
        Tower.msg.started("Deploying " + env.name);
        const deployment_options = [...deploy_options.state].join(",");
        const xhr = new XMLHttpRequest();
        xhr.open(
            "GET",
            `/deploy/${env.id}/?deployment_options=${deployment_options}`,
            true
        );
        xhr.onprogress = () => {
            const text = this.process_output(
                xhr.responseText.substr(offset),
                status,
                clock
            );
            offset = xhr.responseText.length;
            output += text;
            output_panel.setHTML(output);
            output_panel.scrollTo(0, 10000000);
            badges_panel.setValues(status);
        };
        xhr.onload = () => {
            running = false;
            this.on_deploy_complete(status, badges_panel);
        };
        xhr.onerror = () => {
            running = false;
            this.on_deploy_error(status, badges_panel);
        };
        xhr.send();
        this.update_clock(
            clock,
            output_panel,
            start_time,
            () => running
        );
    };

    on_deploy_complete = (status, badges_panel) => {
        if (status.unreach || status.failed) {
            status.status = "<i class='fa fa-bolt'></i> Failed";
            Tower.msg.failed("Deploy failed");
            Tower.notification("Deploy failed");
        } else {
            status.status = "<i class='fa fa-check-circle'></i> Complete";
            Tower.msg.complete("Deploy completed");
            Tower.notification("Deploy completed");
        }
        badges_panel.setValues(status);
    };

    on_deploy_error = (status, badges_panel) => {
        status.status = "<i class='fa fa-bolt'></i> Failed";
        badges_panel.setValues(status);
        Tower.msg.failed("Deploy failed");
        Tower.notification("Deploy failed");
    };

    process_output = (text, status, clock) => {
        const t = webix.template.escape(text);
        let match;
        this.rx_progress.lastIndex = 0;
        while ((match = this.rx_progress.exec(t))) {
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
        if (t.match(/(\.\.\.ignoring)/) && status.failed > 0) {
            status.failed--;
        }
        let result = t.replace(this.rx_task, (x) => {
            x = x.replace(this.rx_stars, "");
            return (
                "<span class='ansible-task' style=white-space:nowrap>" +
                x +
                "<span style='float: right'>" +
                clock.getValues().time +
                "</span></span>"
            );
        });
        result = result.replace(this.rx_line, (x) => {
            let c = x.split(":")[0];
            if (c === "fatal") {
                c = "failed";
            }
            return "<span class='ansible-" + c + "'>" + x + "</span>";
        });
        return result;
    };

    update_clock = (
        clock,
        output_panel,
        start_time,
        is_running
    ) => {
        const dt = Math.floor((Date.now() - start_time) / 1000);
        let s = dt % 60;
        let m = Math.floor(dt / 60);
        s = s >= 10 ? "" + s : "0" + s;
        m = m >= 10 ? "" + m : "0" + m;
        clock.setValues({
            time: m + ":" + s
        });
        if (is_running()) {
            webix.delay(
                () => this.update_clock(
                    clock,
                    output_panel,
                    start_time,
                    is_running
                ),
                output_panel,
                [],
                1000
            );
        }
    };
}

export const environment_deploy_logic = new EnvironmentDeployLogic();

router.push(
    new Route(/^\/environment\/(\d+)\/deploy$/, environment_deploy_logic.on_route, "environment")
);