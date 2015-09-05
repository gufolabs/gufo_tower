Ext.define("Tower.view.environment.List", {
    extend: "Ext.grid.Panel",
    xtype: "app-environment-list",
    requires: [
        "Tower.store.Environment"
    ],
    reference: "grid",
    bind: {
        store: "{environments}",
        selection: "{selectedEnvironment}"
    },
    autoLoad: true,
    columns: [
        {
            text: "Environment",
            dataIndex: "name",
            width: 100
        },
        {
            text: "Type",
            dataIndex: "env_type",
            width: 120,
            renderer: function (v) {
                return {
                    prod: "Productive",
                    test: "Test",
                    dev: "Develop",
                    eval: "Evaluation",
                    other: "Other"
                }[v];
            }
        },
        {
            text: "Description",
            dataIndex: "description",
            flex: 1
        }
    ],
    viewConfig: {
        emptyText: "No environments"
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
                    text: "New Environment",
                    handler: "onCreate"
                }
            ]
        }
    ],
    listeners: {
        itemdblclick: "onItemSelected"
    }
});
