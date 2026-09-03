// ----------------------------------------------------------------------
// Role Form UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import { role_form_logic } from "./logic.js";
import { current_env } from "../../state.js";

export const role_form = {
    id: "role_form_panel",
    rows: [
        {
            view: "toolbar",
            id: "role_form_toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: () => {
                        navigation.navigate(`/environment/${current_env.state.id}/role`);
                    },
                    width: 32
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: role_form_logic.on_save
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: role_form_logic.on_delete
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
                        window.open("/docs/user-guide/role/form/", "_blank");
                    }
                }
            ]
        },
        {
            view: "form",
            id: "role_form",
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
                    placeholder: "Name",
                    invalidMessage: "Cannot be empty"
                },
                {
                    view: "text",
                    name: "role_name",
                    label: "Role name",
                    required: true,
                    placeholder: "Role name",
                    invalidMessage: "Cannot be empty",
                    bottomLabel: "Role name that will be known to Ansible"
                },
                {
                    view: "checkbox",
                    name: "is_enabled",
                    label: "Enabled",
                    value: true,
                    required: true
                },
                {
                    view: "textarea",
                    name: "description",
                    label: "Description",
                    height: 150
                },
                {
                    view: "text",
                    name: "link",
                    label: "Link",
                    required: true,
                    placeholder: "git+https://github.com/bla/blabla@master",
                },
                {}
            ]
        }
    ]
};
