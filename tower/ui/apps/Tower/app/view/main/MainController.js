/**
 * This class is the controller for the main view for the application. It is specified as
 * the "controller" of the Main view class.
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('Tower.view.main.MainController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.main',

    listen: {
        controller: {
            "*": {
                login: "onLogin",
                logout: "onLogout"
            }
        }
    },

    init: function() {
        var me = this;
        // Check the user is logged in
        // Show login or desktop page
        API.Login.is_logged(function(isLogged) {
            me.getView().setActiveItem(isLogged ? 2 : 1);
        });
    },

    onLogin: function () {
        var me = this;
        me.getView().setActiveItem(2);  // Desktop
    },

    onLogout: function () {
        var me = this;
        me.getView().setActiveItem(1);  // Login
    }
});
