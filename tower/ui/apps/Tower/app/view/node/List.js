Ext.define("Tower.view.node.List", {
    extend: "Ext.grid.Panel",
    requires: [
        "Ext.grid.feature.Grouping"
    ],
    xtype: "app-node-list",
    reference: "grid",

    bind: "{nodes}",
    autoLoad: true,
    features: [{
        ftype: "grouping",
        groupHeaderTpl: "{columnName}: {name}",
        hideGroupedHeader: true,
        startCollapsed: false
    }],
    columns: [
        {
            text: "Node",
            dataIndex: "name",
            width: 150
        },
        {
            text: "Datacenter",
            dataIndex: "datacenter",
            renderer: function(v) {
                return v ? v.get("name") : "-";
            }
        },
        {
            text: "Address",
            dataIndex: "address",
            width: 150
        },
        {
            text: "Description",
            dataIndex: "description",
            flex: 1
        }
    ],
    viewConfig: {
        emptyText: "No nodes"
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
                    text: "New Node",
                    handler: "onCreate"
                }
            ]
        }
    ],
    listeners: {
        itemdblclick: "onItemSelected"
    }
});
