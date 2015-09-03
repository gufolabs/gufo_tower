Ext.define('Tower.view.login.LoginController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.login-login',

    // Focus on *user* field
    onFormShow: function() {
        var me = this;
        me.lookupReference("userField").focus();
    },

    onFormLogin: function() {
        var me = this,
            credentials;
        credentials = me.getViewModel().data;
        API.Login.login(credentials, function(isLogged) {
            if(isLogged) {
                me.fireEvent("login");
            } else {
                Ext.Msg.alert("Error", "Invalid credentials");
            }
        });
        me.getView().reset();
    },

    onFormReset: function() {
        var me = this;
        me.getView().reset();
    }
});
