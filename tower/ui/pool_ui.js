var pool_list = {
    id: "pool_list_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "search",
                    placeholder: "Search...",
                    width: 150,
                    on: {
                        "onChange": "pool_logic.on_search"
                    }
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: "pool_logic.on_add"
                }
            ]
        },
        {
            view: "datatable",
            id: "pool_list",
            select: "row",
            url: "rpc->pool",
            columns: [
                {
                    id: "name",
                    header: "Pool",
                    width: 100
                },
                {
                    id: "description",
                    header: "Description",
                    fillspace: true
                }
            ],
            on: {
                onItemDblClick: "pool_logic.on_edit"
            }
        }
    ]
};

var pool_form = {
    id: "pool_form_panel",
    rows: [
        {
            view: "toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    autowidth: true,
                    click: "pool_logic.show_list"
                },
                {},
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: "pool_logic.on_save"
                },
                {},
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: "pool_logic.on_delete"
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
                }
            ]
        }
    ]
};
