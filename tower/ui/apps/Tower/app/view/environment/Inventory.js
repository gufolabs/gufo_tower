Ext.define("Tower.view.environment.Inventory", {
    extend: "Ext.panel.Panel",
    xtype: "app-environment-inventory",
    requires: [
        "Tower.store.Environment"
    ],
    reference: "inventory",
    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            items: [
                {
                    iconCls: "x-fa fa-arrow-left",
                    handler: "onCloseForm"
                }
            ]
        }
    ],
    header: {
        html: "Ansible inventory"
    },
    html: "No data yet",
    autoScroll: true
});
