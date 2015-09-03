Ext.define('Tower.view.login.LoginModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.login-login',
    data: {
        user: "",
        password: ""
    },

    formulas: {
        canReset: function(get) {
            return (get("user").length > 0) || (get("password").length > 0);
        },

        canLogin: function(get) {
            return (get("user").length > 0) && (get("password").length > 0);
        }
    }

});
