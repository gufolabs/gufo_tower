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
                    click: "node_logic.on_add"
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
                    id: "is_enabled",
                    header: "Enabled",
                    width: 70,
                    format: Tower.format.lookup
                },

                {
                    id: "node_type",
                    header: "Type",
                    width: 100,
                    format: Tower.format.lookup
                },
                {
                    id: "datacenter",
                    header: "Datacenter",
                    width: 150,
                    format: Tower.format.lookup
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
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
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
                    width: 32
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
            scroll: false,
            elements: [
                {
                    view: "text",
                    name: "name",
                    label: "Name",
                    required: true,
                    bottomLabel: "Name of server will be replaced with that name",
                    invalidMessage: "Cannot be empty, have to be alphanumeric",
                    validate: Tower.rules.regex(/^[a-zA-Z0-9\.-]*$/)
                },
                {
                    view: "checkbox",
                    name: "is_enabled",
                    label: "Enabled",
                    value: true,
                    required: true,
                },
                {
                    view: "combo",
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
                                view: "combo",
                                name: "node_type",
                                label: "Node Type",
                                options: "rpc->nodetype:lookup",
                                required: true
                            },
                            {
                                view: "text",
                                name: "address",
                                label: "Address",
                                placeholder: "Type node IP address here",
                                required: true,
                                validate: Tower.rules.regex(/[0-9]+.[0-9]+.[0-9]+.[0-9]+(:[0-9]+)?/)
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

