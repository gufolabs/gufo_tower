// ----------------------------------------------------------------------
// Datacenter Form UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import { datacenter_form_logic } from "./logic.js";

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
                    click: () => { navigation.navigate(".."); },
                    width: 32
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: datacenter_form_logic.on_save
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: datacenter_form_logic.on_delete
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
