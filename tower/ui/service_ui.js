var service_panel = {
    id: "service_panel",
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
                    click: "service_logic.on_save"
                },
                {},
                {
                    view: "button",
                    autowidth: true,
                    value: "Expand All",
                    click: function () {
                        service_logic.on_expand_tree(true)
                    }
                },
                {
                    view: "button",
                    autowidth: true,
                    value: "Collapse All",
                    click: function () {
                        service_logic.on_expand_tree(false)
                    }
                },
                {},
                {
                    view: "button",
                    autowidth: true,
                    value: "Group by Node",
                    click: function () {
                        service_logic.on_group_table("node")
                    }
                },
                {
                    view: "button",
                    autowidth: true,
                    value: "Group by Service",
                    click: function () {
                        service_logic.on_group_table("service")
                    }
                }
            ]
        },
        {
            cols: [
                {
                    view: "treetable",
                    collapsed: false,
                    id: "service_list",
                    threeState: true,
                    select: "row",
                    multiselect: true,
                    on: {
                        "onSelectChange": "service_logic.on_select_service",
                        "onAfterLoad": function () {
                            service_logic.on_group_table("service")
                        }
                    },
                    columns:
                        [
                            {id: "service",
                                header: ["Service", {content: "textFilter"}],
                                template: function (obj, common) {
                                    return service_logic.on_column_group(obj,common,"service")
                                },
                                sort: "string",
                                width: 200
                            },
                            {id: "node",
                                header: ["Node", {content: "textFilter"}],
                                template: function (obj, common) {
                                    return service_logic.on_column_group(obj,common,"node")
                                },
                                sort: "string",
                                width: 200
                            },
                            {id: "checked",
                                header: ["Enable", {
                                    content:"customFilterBool",
                                    compare: threeStateCompare
                            }] ,
                                template:function (obj, common) {
                                    return service_logic.set_enabled(obj,common)
                                },
                                width: 120
                            },
                            {id: "pool",
                                header: ["Pool", {content: "selectFilter"}],
                                sort: "string"
                            }
                        ],
                    navigation: true,
                    editable: true,
                    editaction: "click",
                    datafetch: Tower.config.datafetch,
                    loadahead: Tower.config.loadahead
                },
                {
                    view: "form",
                    id: "service_form",
                    header: "config",
                    borderless: true,
                    scroll: true,
                    width: 430,
                    datafetch: Tower.config.datafetch,
                    loadahead: Tower.config.loadahead,
                    elements: []
                }
            ]
        }
    ]
};
