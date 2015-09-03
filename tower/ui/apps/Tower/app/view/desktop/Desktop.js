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
        "Tower.view.about.About"
    ],

    controller: "desktop-desktop",
    viewModel: {
        type: "desktop-desktop"
    },
    ui: "navigation",

    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            items: [
                {
                    xtype: "tbtext",
                    html: "NOC Tower"
                },
                "->",
                {
                    iconCls: "x-fa fa-bars",
                    menu: [
                        {
                            text: "Change Password ...",
                            handler: "onChangePassword"
                        },
                        "-",
                        {
                            text: "Logout",
                            handler: "onLogout"
                        }
                    ]
                }
            ]
        }
    ],

    defaults: {
        bodyPadding: 4
    },

    items: [
        {
            xtype: "app-environment"
        },
        {
            xtype: "app-datacenter"
        },
        {
            title: "Pools"
        },
        {
            title: "Nodes"
        },
        {
            xtype: "app-about"
        }
    ]
});
