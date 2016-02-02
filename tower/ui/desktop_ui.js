var desktop = {
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
                    submenuConfig:{
                        width:200
                    },
                    data: [
                        {
                            id: "user_menu",
                            icon: "user",
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
                                }
                            ]
                        }
                    ],
                    on: {
                        onMenuItemClick: "desktop_logic.on_menu_click"
                    }
                }
            ]
        },
        {
            cols: [
                // Sidebar
                {
                    view: "list",
                    id: "sidebar",
                    width: 200,
                    select: true,
                    scroll: true,
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
                            id: "settings",
                            value: "Settings",
                            icon: "cog"
                        }
                    ],
                    on: {
                        onSelectChange: "desktop_logic.on_select_app",
                        onBeforeSelecT: "desktop_logic.on_before_select_app"
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
