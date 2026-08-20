// ----------------------------------------------------------------------
// Node List UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import { Tower } from "../../lib.js";
import { node_list_logic } from "./logic.js";

export const node_list = {
    id: "node_list_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "search",
                    placeholder: "Search...",
                    width: 150,
                    on: {
                        "onChange": node_list_logic.on_search
                    }
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: () => { navigation.navigate("./new"); }
                }
            ]
        },
        {
            view: "datatable",
            id: "node_list",
            select: "row",
            columns: [
                {
                    id: "name",
                    header: "Node",
                    width: 100
                },
                {
                    id: "is_enabled",
                    header: "Enabled",
                    width: 70,
                    format: Tower.format.check
                },
                {
                    id: "node_type",
                    header: "Type",
                    width: 100,
                    format: Tower.format.lookup
                },
                {
                    id: "datacenter",
                    header: "Datacenter",
                    width: 150,
                    format: Tower.format.lookup
                },
                {
                    id: "address",
                    header: "Address",
                    width: 100
                },
                {
                    id: "description",
                    header: "Description",
                    fillspace: true
                }
            ],
            on: {
                onItemDblClick: (id) => {
                    const item = $$("node_list").getItem(id.row);
                    navigation.navigate(`${location.pathname}/${item.id}`);
                }
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
        }
    ]
};
