
Ext.define("Tower.view.settings.Settings",{
    extend: "Ext.form.Panel",
    xtype: "app-settings",

    requires: [
        "Tower.view.settings.SettingsController"
    ],

    controller: "settings-settings",
    viewModel: {
        type: "settings-settings"
    },

    config: {
        title: "Settings",
        iconCls: "x-fa fa-cog"
    },

    items: [
        {
            xtype: "textfield",
            name: "url",
            fieldLabel: "Base URL",
            anchor: "100%",
            allowBlank: false
        },

        {
            xtype: "textfield",
            name: "repo_url",
            fieldLabel: "Repo URL",
            anchor: "100%",
            allowBlank: false
        }
    ],

    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            items: [
                {
                    text: "Save",
                    iconCls: "x-fa fa-save",
                    handler: "onSave",
                    disabled: true,
                    formBind: true
                }
            ]
        }
    ],
    listeners: {
        activeapp: "onActiveApp"
    }
});
