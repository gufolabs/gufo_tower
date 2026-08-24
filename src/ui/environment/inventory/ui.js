// ----------------------------------------------------------------------
// Environment Inventory UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

export const environment_inventory = {
    id: "environment_inventory_panel",
    rows: [
        {
            view: "toolbar",
            id: "environment_inventory_toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: () => { navigation.navigate("/environment"); },
                    width: 32
                },
                {
                    view: "label",
                    label: "Ansible Inventory"
                },
                {}
            ]
        },
        {
            view: "template",
            id: "environment_inventory_text",
            template: "<pre>#text#</pre>",
            data: {
                text: "?"
            },
            scroll: true
        }
    ]
};
