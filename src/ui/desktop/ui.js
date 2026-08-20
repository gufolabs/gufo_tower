// ----------------------------------------------------------------------
// Desktop UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { home_panel } from "../home/ui.js";
import { environment_list } from "../environment/list/ui.js";
import { environment_form } from "../environment/form/ui.js";
import { environment_inventory } from "../environment/inventory/ui.js";
import { environment_deploy } from "../environment/deploy/ui.js";
import { datacenter_list } from "../datacenter/list/ui.js";
import { datacenter_form } from "../datacenter/form/ui.js";
import { role_list } from "../role/list/ui.js";
import { role_form } from "../role/form/ui.js";
import { pool_list } from "../pool/list/ui.js";
import { pool_form } from "../pool/form/ui.js";
import { node_list } from "../node/list/ui.js";
import { node_form } from "../node/form/ui.js";
import { service_panel } from "../service/ui.js";
import { settings_form } from "../settings/ui.js";
import { desktop_logic } from "./logic.js";
import { version } from "../generated/version.js";
import { short_navigation } from "../nav.js";

export const desktop = {
    id: "desktop",
    rows: [
        // Toolbar
        {
            type: "clean",
            id: "header",
            cols: [
                {
                    view: "toolbar",
                    id: "desktop_header",
                    fillspace: true,
                    elements: [
                        {
                            view: "button",
                            id: "grill",
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
                            label: "Gufo Tower: Select environment"
                        },
                        {
                            view: "menu",
                            id: "desktop_menu",
                            height: "auto",
                            width: 32,
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
                                            id: "version",
                                            icon: "info",
                                            value: `Version: ${version}`
                                        },
                                        {
                                            id: "docs",
                                            icon: "book",
                                            value: "Documentation"
                                        },
                                        { $template: "Separator" },
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
                                    ]
                                }
                            ],
                            on: {
                                onMenuItemClick: desktop_logic.on_menu_click
                            }
                        }
                    ]
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
                    data: short_navigation,
                    on: {
                        onSelectChange: desktop_logic.on_select_app,
                    }
                },
                {
                    view: "multiview",
                    id: "apps",
                    animate: false,
                    cells: [
                        home_panel,
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
