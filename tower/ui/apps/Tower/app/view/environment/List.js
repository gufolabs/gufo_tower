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
            text: "URL",
            dataIndex: "web_host",
            width: 150,
            renderer: function(v) {
                return "<a target='_' href='https://" + v + "/'>" + v + "</a>";
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
                },
                "-",
                {
                    iconCls: "x-fa fa-search",
                    text: "Inventory",
                    handler: "onInventory",
                    bind: {
                        disabled: "{!isEnvironmentSelected}"
                    }
                },
                {
                    iconCls: "x-fa fa-arrow-circle-down",
                    reference: "pullButton",
                    text: "Pull",
                    handler: "onPull",
                    bind: {
                        disabled: "{!isEnvironmentSelected}"
                    }
                },
                {
                    iconCls: "x-fa fa-play",
                    reference: "deployButton",
                    text: "Deploy",
                    handler: "onDeploy",
                    bind: {
                        disabled: "{!isEnvironmentSelected}"
                    }
                }
            ]
        }
    ],
    listeners: {
        itemdblclick: "onItemSelected"
    }
});
