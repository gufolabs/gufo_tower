// ----------------------------------------------------------------------
// Datacenter UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { datacenter_logic } from "./datacenter_logic.js";
import { Tower } from "./lib.js";

export const datacenter_list = {
    id: "datacenter_list_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "search",
                    id: "datacenter_search",
                    placeholder: "Search...",
                    width: 150,
                    on: {
                        "onChange": datacenter_logic.on_search
                    }
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: datacenter_logic.on_add
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
                onItemDblClick: datacenter_logic.on_edit
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
        }
    ]
};

export const datacenter_form = {
    id: "datacenter_form_panel",
    rows: [
        {
            view: "toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: datacenter_logic.show_list,
                    width: 32
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: datacenter_logic.on_save
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: datacenter_logic.on_delete
                },
                {}
            ]
        },
        {
            view: "form",
            id: "datacenter_form",
            elementsConfig: {
                labelWidth: 110
            },
            scroll: false,
            elements: [
                {
                    view: "text",
                    name: "name",
                    label: "Name",
                    required: true,
                    placeholder: "Datacenter name (unique)",
                    invalidMessage: "Cannot be empty"
                },
                {
                    view: "textarea",
                    name: "description",
                    label: "Description",
                    height: 150
                },
                {
                    view: "text",
                    name: "proxy",
                    label: "Internet Proxy",
                    placeholder: "Proxy address:port",
                    bottomLabel: "Format http://user:password@192.168.1.1:3128"
                },
                {}
            ]
        }
    ]
};
