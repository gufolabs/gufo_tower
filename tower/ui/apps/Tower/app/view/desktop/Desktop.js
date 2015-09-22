Ext.define("Tower.view.desktop.Desktop", {
    extend: "Ext.tab.Panel",
    xtype: "app-desktop",

    requires: [
        "Ext.toolbar.TextItem",
        "Ext.form.field.ComboBox",

        "Tower.view.desktop.DesktopController",
        "Tower.view.desktop.DesktopModel",
        "Tower.view.environment.Environment",
        "Tower.view.datacenter.Datacenter",
        "Tower.view.pool.Pool",
        "Tower.view.node.Node",
        "Tower.view.service.Service",
        "Tower.view.settings.Settings",
        "Tower.view.about.About",
        "Tower.store.Environment"
    ],

    controller: "desktop-desktop",
    viewModel: {
        type: "desktop-desktop"
    },
    ui: "navigation",
    tabPosition: "left",
    tabRotation: 0,

    defaults: {
        bodyPadding: 4,
        textAlign: "left"
    },

    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            id: "tower-desktop-header",
            items: [
                {
                    xtype: "tbtext",
                    bind: {
                        html: "NOC Tower: {environmentHeader}"
                    }
                },
                "->",
                {
                    xtype: "combobox",
                    valueField: "id",
                    displayField: "name",
                    emptyText: "Select Environment",
                    width: 200,
                    bind: {
                        store: "{environments}",
                        selection: "{selectedEnvironment}"
                    }
                },
                {
                    iconCls: "x-fa fa-bars",
                    menu: [
                        {
                            text: "Change Password ...",
                            iconCls: "x-fa fa-pencil-square-o",
                            handler: "onChangePassword"
                        },
                        "-",
                        {
                            text: "Logout",
                            iconCls: "x-fa fa-sign-out",
                            handler: "onLogout"
                        }
                    ]
                }
            ]
        }
    ],

    items: [
        {
            xtype: "app-environment"
        },
        {
            xtype: "app-datacenter"
        },
        {
            xtype: "app-pool"
        },
        {
            xtype: "app-node"
        },
        {
            xtype: "app-service"
        },
        {
            title: "Jobs",
            iconCls: "x-fa fa-tasks"
        },
        {
            xtype: "app-settings"
        },
        {
            xtype: "app-about"
        }
    ],

    listeners: {
        tabchange: "onTabChange"
    }
});
