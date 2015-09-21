Ext.define('Tower.view.desktop.DesktopController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.desktop-desktop',
    requires: [
        "Ext.Msg",
        "Tower.view.desktop.ChangePassword"
    ],

    onTabChange: function(tabPanel, newTab, oldTab, eOpts) {
        var me = this;
        oldTab.fireEvent("inactiveapp");
        newTab.fireEvent("activeapp");
    },

    onLogout: function() {
        var me = this;
        API.Login.logout(function() {
            me.fireEvent("logout");
        });
    },

    onChangePassword: function() {
        var me = this;
         me.passChangeForm = Ext.create("Tower.view.desktop.ChangePassword", {
            controller: me
        });
        me.passChangeForm.show();
        me.lookupReference("oldPassword").focus();
    },

    changePassword: function() {
        var me = this,
            op, np, np2;
        op = me.lookupReference("oldPassword").getValue();
        np = me.lookupReference("newPassword").getValue();
        np2 = me.lookupReference("newPassword2").getValue();
        if(np !== np2) {
            Ext.Msg.alert("Error", "Passwords mismatch");
        } else {
            API.Login.change_password(op, np, function(result) {
                if(result) {
                    Ext.Msg.alert("Success", "Password changed");
                    me.passChangeForm.close();
                    delete me.passChangeForm;
                } else {
                    Ext.Msg.alert("Error", "Invalid password");
                }
            });
        }
    }
});
