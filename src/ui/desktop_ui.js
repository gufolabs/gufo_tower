// ----------------------------------------------------------------------
// Desktop UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { environment_list, environment_form, environment_inventory, environment_deploy } from "./environment_ui.js";
import { datacenter_list, datacenter_form } from "./datacenter_ui.js";
import { role_list, role_form } from "./role_ui.js";
import { pool_list, pool_form } from "./pool_ui.js";
import { node_list, node_form } from "./node_ui.js";
import { service_panel } from "./service_ui.js";
import { settings_form } from "./settings_ui.js";
import { desktop_logic } from "./desktop_logic.js";
import { version } from "./generated/version.js";

export const desktop = {
    id: "desktop",
    rows: [
        // Toolbar
        {
            type: "clean",
            cols: [
                {
                    view: "toolbar",
                    id: "desktop_header",
                    fillspace: true,
                    elements: [
                        {
                            view: "button",
                            type: "icon",
                            icon: "bars",
                            width: 37,
                            align: "left",
                            css: "app_button",
                            click: function () {
                                $$("sidebar").toggle()
                            }
                        },
                        {
                            id: "environment_label",
                            view: "label",
                            label: "NOC Tower: Select environment"
                        }
                    ]
                },
                {
                    view: "menu",
                    id: "desktop_menu",
                    height: "auto",
                    width: 50,
                    submenuConfig: {
                        width: 200
                    },
                    data: [
                        {
                            id: "user_menu",
                            icon: "menu_user",
                            css: "app_button",
                            submenu: [
                                {
                                    id: "change_password",
                                    value: "Change Password...",
                                    icon: "key"
                                },
                                {
                                    id: "logout",
                                    value: "Logout",
                                    icon: "sign-out"
                                },
                                {
                                    id: "version",
                                    icon: "info",
                                    value: `Version: ${version}`
                                }
                            ]
                        }
                    ],
                    on: {
                        onMenuItemClick: desktop_logic.on_menu_click
                    }
                }
            ]
        },
        {
            cols: [
                // Sidebar
                {
                    view: "sidebar",
                    id: "sidebar",
                    width: 200,
                    select: true,
                    data: [
                        {
                            id: "environment",
                            value: "Environments",
                            icon: "cloud"
                        },
                        {
                            id: "datacenter",
                            value: "Datacenters",
                            icon: "building"
                        },
                        {
                            id: "pool",
                            value: "Pools",
                            icon: "files-o"
                        },
                        {
                            id: "node",
                            value: "Nodes",
                            icon: "server"
                        },
                        {
                            id: "service",
                            value: "Services",
                            icon: "cubes"
                        },
                        {
                            id: "role",
                            value: "Additional services",
                            icon: "archive"
                        },
                        {
                            id: "settings",
                            value: "Settings",
                            icon: "cog"
                        }
                    ],
                    on: {
                        onSelectChange: desktop_logic.on_select_app.bind(desktop_logic),
                        onBeforeSelect: desktop_logic.on_before_select_app.bind(desktop_logic)
                    }
                },
                {
                    view: "multiview",
                    id: "apps",
                    cells: [
                        environment_list,
                        environment_form,
                        environment_inventory,
                        environment_deploy,
                        datacenter_list,
                        datacenter_form,
                        role_list,
                        role_form,
                        pool_list,
                        pool_form,
                        node_list,
                        node_form,
                        service_panel,
                        settings_form
                    ]
                }
            ]
        }
    ]
};
