// ----------------------------------------------------------------------
// Datacenter List UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { datacenter_list_logic } from "./logic.js";
import { Tower } from "../../lib.js";

export const datacenter_list = {
    id: "datacenter_list_panel",
    rows: [
        {
            view: "toolbar",
            id: "datacenter_list_toolbar",
            elements: [
                // {
                //     view: "search",
                //     id: "datacenter_search",
                //     placeholder: "Search...",
                //     width: 150,
                //     on: {
                //         "onChange": datacenter_list_logic.on_search
                //     }
                // },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: () => navigation.navigate("/datacenter/new")
                },
                {
                    view: "spacer"
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "question-circle",
                    label: "Help",
                    autowidth: true,
                    click: () => {
                        window.open("/docs/user-guide/datacenter/list/", "_blank");
                    }
                }
            ]
        },
        {
            view: "datatable",
            id: "datacenter_list",
            select: "row",
            columns: [
                {
                    id: "name",
                    header: "Datacenter",
                    width: 100,
                    sort: "server"
                },
                {
                    id: "description",
                    header: "Description",
                    fillspace: true
                }
            ],
            on: {
                onItemDblClick: (id) => {
                    const item = $$("datacenter_list").getItem(id.row);
                    navigation.navigate(`${location.pathname}/${item.id}`);
                }
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
        }
    ]
};
