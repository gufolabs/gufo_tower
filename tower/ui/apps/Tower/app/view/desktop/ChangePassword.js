Ext.define("Tower.view.desktop.ChangePassword", {
    extend: "Ext.window.Window",
    requires: [
        "Ext.form.Panel",
        "Ext.form.field.Text"
    ],
    title: "Change Password",
    modal: true,
    width: 320,
    items: [{
        xtype: "form",
        bodyPadding: 4,
        defaults: {
            anchor: "100%"
        },
        items: [
            {
                xtype: "textfield",
                name: "oldPassword",
                fieldLabel: "Old Password",
                allowBlank: false,
                reference: "oldPassword",
                inputType: "password"
            },
            {
                xtype: "textfield",
                name: "newPassword",
                fieldLabel: "New Password",
                allowBlank: false,
                reference: "newPassword",
                inputType: "password"
            },
            {
                xtype: "textfield",
                name: "newPassword2",
                fieldLabel: "New Password (Retype)",
                allowBlank: false,
                reference: "newPassword2",
                inputType: "password"
            }
        ],
        buttons: [
            {
                text: "Change Password",
                handler: "changePassword",
                formBind: true
            }
        ]
    }]
});
