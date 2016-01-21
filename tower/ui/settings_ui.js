var settings_form = {
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
                    click: "settings_logic.on_save"
                }
            ]
        },
        {
            view: "form",
            id: "settings_form",
            elements: [
                {
                    view: "text",
                    name: "installation_name",
                    label: "Tower Name",
                    labelWidth: 110,
                    required: true,
                    invalidMessage: "Tower name cannot be empty"
                },
                {
                    view: "text",
                    name: "url",
                    label: "Tower URL",
                    labelWidth: 110,
                    required: true,
                    invalidMessage: "Tower URL cannot be empty"
                },
                {
                    view: "text",
                    name: "repo_url",
                    label: "Repo URL",
                    labelWidth: 110,
                    required: true,
                    invalidMessage: "Repo URL cannot be empty"
                },
                {}
            ]
        }
    ]
};
