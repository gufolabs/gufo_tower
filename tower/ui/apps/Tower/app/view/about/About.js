Ext.define("Tower.view.about.About", {
    extend: "Ext.panel.Panel",
    xtype: "app-about",

    requires: [
        "Tower.view.about.AboutController",
        "Tower.view.about.AboutModel"
    ],

    controller: "about-about",
    viewModel: {
        type: "about-about"
    },

    config: {
        title: "About",
        iconCls: "x-fa fa-info-circle",
        html: "Hello, World!!"
    }
});
