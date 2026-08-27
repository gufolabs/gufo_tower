// ----------------------------------------------------------------------
// Pool UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { pool_list_logic } from "./logic.js";
import { Tower } from "../../lib.js";
export const pool_list = {
    id: "pool_list_panel",
    rows: [
        {
            view: "toolbar",
            id: "pool_list_toolbar",
            elements: [
                // {
                //     view: "search",
                //     placeholder: "Search...",
                //     width: 150,
                //     on: {
                //         "onChange": pool_list_logic.on_search
                //     }
                // },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: () => { navigation.navigate(`${location.pathname}/new`); }
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
                        window.open("/docs/user-guide/pool/list/", "_blank");
                    }
                }
            ]
        },
        {
            view: "datatable",
            id: "pool_list",
            select: "row",
            columns: [
                {
                    id: "name",
                    header: "Pool",
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
                    const item = $$("pool_list").getItem(id.row);
                    navigation.navigate(`${location.pathname}/${item.id}`)
                }
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
        }
    ]
};

