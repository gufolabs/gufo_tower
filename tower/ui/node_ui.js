var node_list = {
    id: "node_list_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "search",
                    placeholder: "Search...",
                    width: 150,
                    on: {
                        "onChange": "node_logic.on_search"
                    }
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: "datacenter_logic.on_add"
                }
            ]
        },
        {
            view: "datatable",
            id: "node_list",
            select: "row",
            columns: [
                {
                    id: "name",
                    header: "Node",
                    width: 100
                },
                {
                    id: "datacenter",
                    header: "Datacenter",
                    width: 150
                },
                {
                    id: "address",
                    header: "Address",
                    width: 100
                },
                {
                    id: "description",
                    header: "Description",
                    fillspace: true
                }
            ],
            on: {
                onItemDblClick: "node_logic.on_edit"
            }
        }
    ]
};

var node_form = {
    id: "node_form_panel",
    rows: [
        {
            view: "toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: "node_logic.show_list",
                    width: 20
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: "node_logic.on_save"
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: "node_logic.on_delete"
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
            scroll: true,
            elements: [
                {
                    view: "text",
                    name: "name",
                    label: "Name",
                    required: true,
                    validate: Tower.rules.regex(/^[a-zA-Z][a-zA-Z0-9\-_]*$/)
                },
                //{
                //    view: "combo",
                //    name: "datacenter",
                //    label: "Datacenter",
                //    //@!@
                //    required: true
                //},
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
                            //{
                            //    view: "combo",
                            //    name: "node_type",
                            //    label: "Node Type",
                            //    // @!@
                            //    allowBlank: false
                            //},
                            {
                                view: "text",
                                name: "address",
                                label: "Address",
                                required: true
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

