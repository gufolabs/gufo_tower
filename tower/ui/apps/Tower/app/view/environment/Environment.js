Ext.define("Tower.view.environment.Environment", {
    extend: "Ext.panel.Panel",
    xtype: "app-environment",

    requires: [
        "Tower.view.environment.EnvironmentController",
        "Tower.view.environment.EnvironmentModel",
        "Tower.view.environment.List",
        "Tower.view.environment.Form",
        "Tower.view.environment.Inventory",
        "Tower.view.environment.Deploy"
    ],

    controller: "environment-environment",
    viewModel: {
        type: "environment-environment"
    },

    config: {
        title: "Environments",
        iconCls: "x-fa fa-cloud"
    },

    layout: "card",

    items: [
        {
            xtype: "app-environment-list"
        },
        {
            xtype: "app-environment-form"
        },
        {
            xtype: "app-environment-inventory"
        },
        {
            xtype: "app-environment-deploy"
        }
    ]
});
