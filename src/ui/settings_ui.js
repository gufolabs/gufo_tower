import { settings_logic } from "./settings_logic.js";
export const settings_form = {
    id: "settings_form_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: settings_logic.on_save
                }
            ]
        },
        {
            view: "form",
            id: "settings_form",
            elements: [
                {
                    view: "text",
                    labelWidth: 150,
                    name: "installation_name",
                    label: "Tower Name",

                    required: true,
                    invalidMessage: "Tower name cannot be empty"
                },
                {
                    view: "text",
                    name: "url",
                    labelWidth: 150,
                    label: "Tower URL",
                    required: true,
                    invalidMessage: "Tower URL cannot be empty"
                },
                {
                    view: "segmented",
                    name: "group_by",
                    labelWidth: 150,
                    label: "Group services by",
                    value: "node",
                    options: [
                        { value: "service" },
                        { value: "node" }
                    ]
                },
                {}
            ]
        }
    ]
};
