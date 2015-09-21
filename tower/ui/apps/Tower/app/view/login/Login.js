Ext.define("Tower.view.login.Login", {
    extend: "Ext.panel.Panel",

    requires: [
        "Tower.view.login.LoginController",
        "Tower.view.login.LoginModel"
    ],

    xtype: "app-login",

    controller: "login-login",
    viewModel: {
        type: "login-login"
    },
    layout: "center",

    items: [{
        xtype: "form",
        width: 400,
        title: "Login to the NOC Tower",
        bodyPadding: 4,

        defaults: {
            anchor: "100%",
            labelWidth: 80
        },

        items: [
            {
                name: "user",
                xtype: "textfield",
                itemId: "user",
                fieldLabel: "User",
                emptyText: "User Id",
                allowBlank: false,
                bind: "{user}",
                reference: "userField"
            },
            {
                name: "password",
                xtype: "textfield",
                inputType: "password",
                fieldLabel: "Password",
                emptyText: "Enter password",
                allowBlank: false,
                bind: "{password}"
            }
        ],

        buttons: [
            {
                text: "Login",
                handler: "onFormLogin",
                formBind: true
            },
            {
                text: "Reset",
                handler: "onFormReset"
            }
        ]
    }],

    listeners: {
        show: "onFormShow"
    }
});
