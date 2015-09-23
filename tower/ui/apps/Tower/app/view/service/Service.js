
Ext.define("Tower.view.service.Service",{
    extend: "Ext.panel.Panel",
    xtype: "app-service",

    requires: [
        "Tower.view.service.ServiceController",
        "Tower.view.service.ServiceModel",
        "Tower.view.service.List",
        "Tower.view.service.Pivot"
    ],

    controller: "service-service",
    viewModel: {
        type: "service-service"
    },

    config: {
        title: "Services",
        iconCls: "x-fa fa-cubes"
    },

    layout: "card",
    bind: {
        disabled: "{!isEnvironmentSelected}"
    },

    items: [
        {
            xtype: "app-service-list"
        },
        {
            xtype: "app-service-pivot"
        }
    ],

    listeners: {
        activeapp: "onActiveApp"
    }
});
