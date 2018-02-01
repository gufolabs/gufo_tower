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
                        service_logic.on_expand_tree("true")
                    }
                },
                {
                    view: "button",
                    autowidth: true,
                    value: "Collapse All",
                    click: function () {
                        service_logic.on_expand_tree("false")
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
            view: "accordion",
            multi: true,
            cols: [
                {
                    view: "treetable",
                    collapsed: false,
                    id: "service_list",
                    threeState: true,
                    select: "row",
                    multiselect: true,
                    on: {
                        "onSelectChange": "service_logic.on_select_service"
                    },
                    columns:
                        [
                            {
                                id: "service",
                                header: ["Service", {content: "textFilter"}],
                                template: function (obj, common) {
                                    var parent = obj.$parent ? obj.$parent.split("$")[1] : undefined;
                                    if (obj.$group && obj.service) {
                                        return common.space(obj, common) +
                                            common.icon(obj, common) +
                                            common.folder(obj, common) +
                                            "<span>" + obj.service + "</span>"
                                    } else if (parent !== obj.service) {
                                        return obj.service
                                    } else {
                                        return ""
                                    }
                                },
                                css: "column_text",
                                width: 200
                            },
                            {
                                id: "node",
                                header: ["Node", {content: "textFilter"}],
                                template: function (obj, common) {
                                    var parent = obj.$parent ? obj.$parent.split("$")[1] : undefined;
                                    if (obj.$group && obj.node) {
                                        return common.space(obj, common) +
                                            common.icon(obj, common) +
                                            common.folder(obj, common) +
                                            "<span>" + obj.node + "</span>"
                                    } else if (parent !== obj.node) {
                                        return obj.node;
                                    } else {
                                        return ""
                                    }
                                },
                                css: "column_text",
                                sort: "string",
                                autowidth: true
                            },
                            {id: "present",
                                header: "Enable",
                                template:"{common.treecheckbox()}",
                                editor:"checkbox",
                                width: 80
                            },
                            {id: "pool", header: ["Pool", {content: "selectFilter"}]}
                        ],
                    ready: "service_logic.on_group_table",
                    navigation: true,
                    editable: true,
                    editaction: "click",
                    datafetch: Tower.config.datafetch,
                    loadahead: Tower.config.loadahead
                },
                {
                    view: "form",
                    id: "service_form",
                    collapsed: true,
                    header: "config",
                    borderless: true,
                    scroll: true,
                    width: 442,
                    elements: []
                }
            ]
        }
    ]
};
