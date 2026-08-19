// ----------------------------------------------------------------------
// Environment List UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { environment_list_logic } from "./logic.js";
import { Tower } from "../../lib.js";

export const environment_list = {
    id: "environment_list_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "search",
                    placeholder: "Search...",
                    width: 150,
                    on: {
                        "onChange": environment_list_logic.on_search
                    }
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: () => navigation.navigate("/environment/new")
                },
                {
                    view: "button",
                    id: "environment_inventory_button",
                    type: "icon",
                    icon: "search",
                    label: "Inventory",
                    click: () => {
                        const id = $$("environment_list").getSelectedId();
                        const env = $$("environment_list").getItem(id);
                        navigation.navigate(`./${env.id}/inventory`);
                    },
                    autowidth: true,
                    disabled: true
                },
                {
                    view: "button",
                    id: "environment_pull_button",
                    type: "icon",
                    icon: "arrow-circle-down",
                    label: "Pull",
                    click: environment_list_logic.on_pull,
                    autowidth: true,
                    disabled: true
                },
                {
                    view: "button",
                    id: "environment_deploy_button",
                    type: "icon",
                    icon: "play",
                    label: "Deploy",
                    click: () => {
                        const id = $$("environment_list").getSelectedId();
                        const env = $$("environment_list").getItem(id);
                        navigation.navigate(`./${env.id}/deploy`);
                    },
                    autowidth: true,
                    disabled: true,
                    tooltip: "Stop all daemons, update everything, restart everything"
                },
                {
                    view: "multiselect",
                    label: "Deploy options",
                    id: "deployment_options",
                    labelWidth: 100,
                    options: [
                        {
                            id: 1,
                            value: "Install Everything",
                            tooltip: "Ignore other options except verbose. Normal install"
                        },
                        { id: 93, value: "Run pre deploy checks" },
                        { id: 94, value: "Run post deploy tests" },
                        { id: 50, value: "Restart quick", tooltip: "Stop all, start all" },
                        { id: 51, value: "Restart gentle", tooltip: "Restart one by one" },
                        { id: 90, value: "Be verbose", tooltip: "Debug output -v" },
                        { id: 91, value: "Be extremely verbose", tooltip: "Debug output -vvvv" },
                        { id: 92, value: "Show secrets in deploy log", tooltip: "Disable no_log" }
                    ],
                    value: "1,93,94"
                }

            ]
        },
        {
            view: "datatable",
            id: "environment_list",
            select: "row",
            columns: [
                {
                    id: "name",
                    header: "Environment",
                    width: 100,
                    sort: "server"
                },
                {
                    id: "env_type",
                    header: "Type",
                    width: 120
                },
                {
                    id: "web_host",
                    header: "URL",
                    width: 150,
                    format: function (v) {
                        return "<a target='_' href='https://" + v + "/'>" + v + "</a>";
                    }
                },
                {
                    id: "description",
                    header: "Description",
                    fillspace: true
                }
            ],
            on: {
                onSelectChange: environment_list_logic.on_select,
                onItemDblClick: (id) => {
                    const item = $$("environment_list").getItem(id.row);
                    navigation.navigate(`./${item.id}`);
                }
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
        }
    ]
};