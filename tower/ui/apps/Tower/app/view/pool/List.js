Ext.define("Tower.view.pool.List", {
    extend: "Ext.grid.Panel",
    xtype: "app-pool-list",
    reference: "grid",

    bind: "{pools}",
    autoLoad: true,
    columns: [
        {
            text: "Pool",
            dataIndex: "name",
            width: 100
        },
        {
            text: "Description",
            dataIndex: "description",
            flex: 1
        }
    ],
    viewConfig: {
        emptyText: "No pools"
    },
    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            items: [
                {
                    xtype: "textfield",
                    width: 150,
                    emptyText: "Enter search terms ..."
                },
                {
                    iconCls: "x-fa fa-refresh",
                    handler: "onRefresh"
                },
                "-",
                {
                    iconCls: "x-fa fa-plus",
                    text: "New Pool",
                    handler: "onCreate"
                }
            ]
        }
    ],
    listeners: {
        itemdblclick: "onItemSelected"
    }
});
