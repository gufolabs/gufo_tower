Ext.define('Tower.view.desktop.DesktopController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.desktop-desktop',

    onLogout: function() {
        var me = this;
        API.Login.logout(function() {
            me.fireEvent("logout");
        });
    },

    onChangePassword: function() {
        var me = this;
        // @todo: Show form
        Ext.Msg.alert("X", "Change password");
    }
});
