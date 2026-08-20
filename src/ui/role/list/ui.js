// ----------------------------------------------------------------------
// Role List UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { Tower } from "../../lib.js";
import { role_list_logic } from "./logic.js";

export const role_list = {
    id: "role_list_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "search",
                    id: "role_search",
                    placeholder: "Search...",
                    width: 150,
                    on: {
                        "onChange": role_list_logic.on_search
                    }
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: () => { navigation.navigate(`${location.pathname}/new`); }
                }
            ]
        },
        {
            view: "datatable",
            id: "role_list",
            select: "row",
            columns: [
                {
                    id: "name",
                    header: "Name",
                    width: 150
                },
                {
                    id: "role_name",
                    header: "Role Name",
                    width: 150
                },
                {
                    id: "is_enabled",
                    header: "Enabled",
                    format: Tower.format.check
                },
                {
                    id: "description",
                    header: "Description",
                    fillspace: true
                },
                {
                    id: "link",
                    header: "Link",
                    width: 250
                }
            ],
            on: {
                onItemDblClick: (id) => {
                    const item = $$("role_list").getItem(id.row);
                    navigation.navigate(`${location.pathname}/${item.id}`)
                }
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
        }
    ]
};

