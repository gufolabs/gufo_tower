Ext.define("Tower.view.node.Node", {
    extend: "Ext.panel.Panel",
    xtype: "app-node",

    requires: [
        "Tower.view.node.NodeController",
        "Tower.view.node.NodeModel",
        "Tower.view.node.List",
        "Tower.view.node.Form"
    ],

    controller: "node-node",
    viewModel: {
        type: "node-node"
    },

    config: {
        title: "Nodes",
        iconCls: "x-fa fa-server"
    },

    layout: "card",
    bind: {
        disabled: "{!isEnvironmentSelected}"
    },

    items: [
        {
            xtype: "app-node-list"
        },
        {
            xtype: "app-node-form"
        }
    ]
});
