// ----------------------------------------------------------------------
// Environment List logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { app_logic } from "../../app/logic.js";
import { Tower } from "../../lib.js";
import { Route } from "../../route.js";

export class EnvironmentListLogic {
    PULL_CHECK_INTERVAL = 1000;

    init = () => {
        webix.extend($$("environment_list"), webix.ProgressBar);
    };

    on_route = () => {
        $$("environment_list_panel").show();
        this.load();
    };

    // Load data info list
    load = () => {
        $$("environment_list").load("rpc->environment");
    };

    on_select = () => {
        const data = $$("environment_list").getSelectedItem();
        app_logic.select_environment(data);
        $$("environment_inventory_button").enable();
        $$("environment_pull_button").enable();
        $$("environment_deploy_button").enable();
        $$("deployment_options").enable();
    };

    on_search = (nv, ov) => {
    };

    on_pull = () => {
        const env_id = app_logic.current_env.id;
        const check_status = function (env, job_id) {
            API.pull.get_job_status(env, job_id).then(
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
                        webix.delay(check_status, environment_list_logic,
                            [env, job_id],
                            environment_list_logic.PULL_CHECK_INTERVAL);
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
                webix.delay(check_status, environment_list_logic,
                    [env_id, result.job],
                    environment_list_logic.PULL_CHECK_INTERVAL);
            },
            function (err) {
                $$("environment_list").hideProgress();
                Tower.msg.failed("Cannot pull repo");
            }
        );
    };
};

export const environment_list_logic = new EnvironmentListLogic();

export const environment_list_routes = [
    new Route(/^\/environment$/, environment_list_logic.on_route, "environment"),
];