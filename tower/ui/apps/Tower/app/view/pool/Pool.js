
Ext.define("Tower.view.pool.Pool",{
    extend: "Ext.panel.Panel",
    xtype: "app-pool",

    requires: [
        "Tower.view.pool.PoolController",
        "Tower.view.pool.PoolModel",
        "Tower.view.pool.List",
        "Tower.view.pool.Form"
    ],

    controller: "pool-pool",
    viewModel: {
        type: "pool-pool"
    },

    config: {
        title: "Pools",
        iconCls: "x-fa fa-files-o"
    },

    layout: "card",
    bind: {
        disabled: "{!isEnvironmentSelected}"
    },

    items: [
        {
            xtype: "app-pool-list"
        },
        {
            xtype: "app-pool-form"
        }
    ]
});
