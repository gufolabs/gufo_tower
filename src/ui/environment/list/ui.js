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
            id: "environment_list_toolbar",
            elements: [
                // {
                //     view: "search",
                //     placeholder: "Search...",
                //     width: 150,
                //     on: {
                //         "onChange": environment_list_logic.on_search
                //     }
                // },
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
                        navigation.navigate(`/environment/${env.id}/inventory`);
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
                        navigation.navigate(`/environment/${env.id}/deploy`);
                    },
                    autowidth: true,
                    disabled: true
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
                    navigation.navigate(`${location.pathname}/${item.id}`);
                }
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
        }
    ]
};