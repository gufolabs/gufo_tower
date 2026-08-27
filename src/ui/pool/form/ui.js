// ----------------------------------------------------------------------
// Pool form UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import { pool_form_logic } from "./logic.js";
import { current_env } from "../../state.js";

export const pool_form = {
    id: "pool_form_panel",
    rows: [
        {
            view: "toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    width: 32,
                    click: () => {
                        navigation.navigate(`/environment/${current_env.state.id}/pool`);
                    },
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: pool_form_logic.on_save
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: pool_form_logic.on_delete
                },
                {}
            ]
        },
        {
            view: "form",
            id: "pool_form",
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
                    placeholder: "Environment name",
                    invalidMessage: "Cannot be empty"
                },
                {
                    view: "textarea",
                    name: "description",
                    label: "Description",
                    height: 150
                },
                {}
            ]
        }
    ]
};
