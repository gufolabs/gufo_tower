var role_list = {
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
                        "onChange": "role_logic.on_search"
                    }
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: "role_logic.on_add"
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
                    header: "Role",
                    width: 100,
                    sort: "server"
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
                    width: 250,
                }
            ],
            on: {
                onItemDblClick: "role_logic.on_edit"
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
        }
    ]
};

var role_form = {
    id: "role_form_panel",
    rows: [
        {
            view: "toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: "role_logic.show_list",
                    width: 32
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: "role_logic.on_save"
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: "role_logic.on_delete"
                },
                {}
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
                    placeholder: "Role name",
                    invalidMessage: "Cannot be empty"
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
                    bottomLabel: "Link repo format is <a href=https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support>written here</a>"
                },
                {}
            ]
        }
    ]
};
