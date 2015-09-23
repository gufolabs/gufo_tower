Ext.define("Tower.view.service.Pivot", {
    extend: "Ext.panel.Panel",
    xtype: "app-service-pivot",
    autoScroll: true,

    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            items: [
                {
                    iconCls: "x-fa fa-arrow-left",
                    handler: "onClosePivot"
                }
            ]
        }
    ]
});
