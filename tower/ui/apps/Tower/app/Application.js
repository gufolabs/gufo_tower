/**
 * The main application class. An instance of this class is created by app.js when it
 * calls Ext.application(). This is the ideal place to handle application launch and
 * initialization details.
 */
Ext.define('Tower.Application', {
    extend: 'Ext.app.Application',
    requires: [
        "Ext.direct.Manager",
        "Ext.direct.RemotingProvider"
    ],

    name: 'Tower',

    stores: [
        // TODO: add global / shared stores here
    ],

    init: function() {
        // Global _TowerAPI populated by microloader
        // (See app.json for details)
        // Initialize Ext.Direct API
        Ext.direct.Manager.addProvider(window._TowerAPI);
        delete window._TowerAPI;  // Cleanup
    },

    launch: function () {
    },

    onAppUpdate: function () {
        Ext.Msg.confirm('Application Update', 'This application has an update, reload?',
            function (choice) {
                if (choice === 'yes') {
                    window.location.reload();
                }
            }
        );
    }
});
