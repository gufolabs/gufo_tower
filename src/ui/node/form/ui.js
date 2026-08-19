// ----------------------------------------------------------------------
// Node Form UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import { Tower } from "../../lib.js";
import { node_form_logic } from "./logic.js";

export const node_form = {
    id: "node_form_panel",
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
                    click: node_form_logic.on_save
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: node_form_logic.on_delete
                },
                {}
            ]
        },
        {
            view: "form",
            id: "node_form",
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
                    bottomLabel: "Hostname of server will be replaced with that name. Along with ip address will be placed to /etc/hosts",
                    invalidMessage: "Cannot be empty, have to be alphanumeric",
                    validate: Tower.rules.regex(/^[a-zA-Z0-9_.-]*[a-zA-Z0-9]$/)
                },
                {
                    view: "checkbox",
                    name: "is_enabled",
                    label: "Enabled",
                    value: true,
                    required: true,
                },
                {
                    view: "select",
                    name: "datacenter",
                    label: "Datacenter",
                    options: "rpc->datacenter:lookup",
                    required: true
                },
                {
                    view: "textarea",
                    name: "description",
                    label: "Description",
                    height: 150
                },
                {
                    view: "fieldset",
                    label: "Connect",
                    body: {
                        cols: [
                            {
                                view: "select",
                                name: "node_type",
                                label: "Node Type",
                                options: "rpc->nodetype:lookup",
                                required: true
                            },
                            {
                                view: "text",
                                name: "address",
                                label: "IP Address",
                                placeholder: "Type node IP address here",
                                bottomLabel: "Will be placed to /etc/hosts",
                                required: true,
                                invalidMessage: "Node address have to be valid address.",
                                validate: Tower.rules.regex(/^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$/)
                            },
                            {
                                view: "text",
                                name: "login_as",
                                label: "Login As",
                                required: true,
                                value: "ansible"
                            }
                        ]
                    }
                },
                {}
            ]
        }
    ]
};
