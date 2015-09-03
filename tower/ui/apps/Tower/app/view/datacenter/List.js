Ext.define("Tower.view.datacenter.List", {
    extend: "Ext.grid.Panel",
    xtype: "app-datacenter-list",
    requires: [
        "Tower.store.Datacenter"
    ],
    reference: "grid",

    store: {
        type: "datacenter"
    },
    autoLoad: true,
    columns: [
        {
            text: "Datacenter",
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
        emptyText: "No datacenters"
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
                    text: "New Datacenter",
                    handler: "onCreate"
                }
            ]
        }
    ],
    listeners: {
        select: "onItemSelected"
    }
});
