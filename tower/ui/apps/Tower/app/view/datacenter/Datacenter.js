
Ext.define("Tower.view.datacenter.Datacenter",{
    extend: "Ext.panel.Panel",
    xtype: "app-datacenter",

    requires: [
        "Tower.view.datacenter.DatacenterController",
        "Tower.view.datacenter.DatacenterModel",
        "Tower.view.datacenter.List",
        "Tower.view.datacenter.Form"
    ],

    controller: "datacenter-datacenter",
    viewModel: {
        type: "datacenter-datacenter"
    },

    config: {
        title: "Datacenters",
        iconCls: "x-fa fa-building"
    },

    layout: "card",

    items: [
        {
            xtype: "app-datacenter-list"
        },
        {
            xtype: "app-datacenter-form"
        }
    ]
});
