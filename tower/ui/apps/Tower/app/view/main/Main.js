/**
 * This class is the main view for the application. It is specified in app.js as the
 * "mainView" property. That setting automatically applies the "viewport"
 * plugin causing this view to become the body element (i.e., the viewport).
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('Tower.view.main.Main', {
    extend: 'Ext.container.Container',
    xtype: 'app-main',

    requires: [
        'Ext.plugin.Viewport',
        'Ext.window.MessageBox',

        'Tower.view.main.MainController',
        'Tower.view.main.MainModel',

        'Tower.view.init.Init',
        'Tower.view.login.Login',
        'Tower.view.desktop.Desktop'
    ],

    controller: 'main',
    viewModel: 'main',
    layout: "card",

    items: [
        {
            xtype: "app-init"
        },
        {
            xtype: "app-login"
        },
        {
            xtype: "app-desktop"
        }
    ]
});
