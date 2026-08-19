// ----------------------------------------------------------------------
// Home logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../rpc.js";
import { Route } from "../route.js";

export class HomeLogic {
    init = () => {
    };

    on_route = () => {
        this.show();
    };

    show = () => {
        $$("home_panel").show();
        this.load();
    };

    load = () => {
        API.home.get_data().then((data) => {
            this.render(data);
        });
    };

    render = (data) => {
        console.log(">>>", data);
        $$("home_panel").define("template", `
            <div class="home">
                ${this.render_welcome(data)}
                ${this.render_environments(data.environments)}
                ${this.render_summary(data)}
            </div>
        `);
        $$("home_panel").refresh();
    };

    render_welcome = (data) => `
        <h1>Welcome to Gufo Tower</h1>

        <p>
            Gufo Tower is an application for configuring and managing NOC deployments.
        </p>

        <p>
            <a href="/docs/" target="_blank"><i class="fa fa-book"></i> Documentation</a>
                    &nbsp;
            <a href="${data.github}" target="_blank">
                <i class="fa fa-github"></i>GitHub
            </a>
        </p>`;

    render_environments = (environments) => `
    <h2>Environments</h2>

    <table>
        <thead>
            <tr>
                <th>Env. Name</th>
                <th>URL</th>
                <th>Type</th>
                <th>Installation name</th>
                <th>Pools</th>                
                <th>DC</th>
                <th>Nodes</th>
            </tr>
        </thead>
        <tbody>
            ${environments.map((environment) => `
                <tr>
                    <td>${environment.name}</td>
                    <td>
                        <a href="${environment.url}" target="_blank">
                            ${environment.web_host}
                        </a>
                    </td>
                    <td>${environment.env_type}</td>
                    <td>${environment.installation_name}</td>
                    <td>${environment.pools || "-"}</td>
                    <td>${environment.datacenters || "-"}</td>
                    <td>${environment.nodes || "-"}</td>
                </tr>
            `).join("")}
        </tbody>
    </table>`;

    render_summary = (data) => `
    <h2>Summary</h2>
    
    <div class="summary">
    <div>Version:</div>
    <div>${data.version}</div>
    <div>DB Size:</div>
    <div>${data.db_size}</div>
    <div>Home Size:</div>
    <div>${data.home_size}</div>
    `;
};

export const home_logic = new HomeLogic();

export const home_routes = [
    new Route(/^\/$/, home_logic.on_route, "home"),
];