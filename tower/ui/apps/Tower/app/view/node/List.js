Ext.define("Tower.view.node.List", {
    extend: "Ext.grid.Panel",
    xtype: "app-node-list",
    reference: "grid",

    bind: "{nodes}",
    autoLoad: true,
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
                if(!v) {
                    return "-";
                }
                if(v.get) {
                    return v.get("name");
                } else {
                    return "" + v;
                }
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
