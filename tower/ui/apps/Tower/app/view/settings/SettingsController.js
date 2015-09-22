Ext.define('Tower.view.settings.SettingsController', {
    extend: 'Ext.app.ViewController',
    requires: [
        "Ext.window.Toast"
    ],
    alias: 'controller.settings-settings',

    onActiveApp: function() {
        var me = this;
        API.Settings.get_settings(function(result) {
            me.getView().getForm().setValues(result);
        });
    },

    onSave: function() {
        var me = this,
            data;
        data = me.getView().getForm().getValues();
        API.Settings.save_settings(data, function(result) {
            if(result.success) {
                Ext.toast({
                    html: "Settings saved",
                    align: "t"
                });
            } else {
                Ext.toast({
                    html: "Failed to save",
                    align: "t"
                });
            }
        })
    }
});
