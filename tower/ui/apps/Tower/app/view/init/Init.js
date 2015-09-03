
Ext.define("Tower.view.init.Init",{
    extend: "Ext.panel.Panel",
    xtype: "app-init",

    requires: [
        "Tower.view.init.InitController",
        "Tower.view.init.InitModel"
    ],

    controller: "init-init",
    viewModel: {
        type: "init-init"
    },

    html: "Connecting to server"
});
