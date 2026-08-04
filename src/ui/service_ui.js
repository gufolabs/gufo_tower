// ----------------------------------------------------------------------
// Service ui
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { threeStateCompare } from "./lib.js";
import { service_logic } from "./service_logic.js";
import { Tower } from "./lib.js";
export const service_panel = {
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
                    click: service_logic.on_save
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
                    gravity: 2,
                    fillspace: true,
                    multiselect: true,
                    on: {
                        "onSelectChange": service_logic.on_select_service,
                        "onAfterLoad": function () {
                            service_logic.on_group_table("init")
                        }
                    },
                    columns:
                        [
                            {
                                id: "service",
                                header: ["Service", { content: "textFilter" }],
                                template: function (obj, common) {
                                    return service_logic.on_column_group(obj, common, "service")
                                },
                                sort: "string",
                                width: 200,
                                fillspace: 2
                            },
                            {
                                id: "node",
                                header: ["Node", { content: "textFilter" }],
                                template: function (obj, common) {
                                    return service_logic.on_column_group(obj, common, "node")
                                },
                                sort: "string",
                                width: 200,
                                fillspace: 2
                            },
                            {
                                id: "checked",
                                header: ["Enable", {
                                    content: "customFilterBool",
                                    compare: threeStateCompare
                                }],
                                template: function (obj, common) {
                                    return service_logic.set_enabled(obj, common)
                                },
                                width: 120,
                                fillspace: 1
                            },
                            {
                                id: "pool",
                                header: ["Pool", { content: "selectFilter" }],
                                sort: "string",
                                fillspace: 1
                            }
                        ],
                    navigation: true,
                    editable: true,
                    editaction: "click",
                    datafetch: Tower.config.datafetch,
                    loadahead: Tower.config.loadahead
                },
                { view: "resizer" },
                {
                    view: "form",
                    id: "service_form",
                    borderless: true,
                    scroll: true,
                    gravity: 1,
                    minWidth: 430,
                    datafetch: Tower.config.datafetch,
                    loadahead: Tower.config.loadahead,
                    elements: [
                        // {
                        //     view: "scrollview",
                        //     id: "scrollview",
                        //     scroll: "y",
                        //     height: 160,
                        //     width: 150,
                        //     body: {
                        //         rows: [
                        //             {
                        //                 template: "Select row on the left panel and enable it on selected node. \n" +
                        //                 "You can sort thet list with buttons on the tollbar.\n" +
                        //                 "All services have dafault instance count. "
                        //             }
                        //         ]
                        //     }
                        // }
                    ]
                }
            ]
        }
    ]
};
