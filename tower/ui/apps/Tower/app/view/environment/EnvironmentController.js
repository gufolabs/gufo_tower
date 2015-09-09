Ext.define('Tower.view.environment.EnvironmentController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.environment-environment',

    showGrid: function() {
        var me = this;
        me.getView().getLayout().setActiveItem(0);
    },

    showForm: function() {
        var me = this;
        me.getView().getLayout().setActiveItem(1);
    },

    onItemSelected: function(sender, record) {
        var me = this,
            form;
        form = me.lookupReference("form").getForm();
        form.reset();
        form.setValues(record.getData());
        me.getViewModel().set("record", record);
        me.showForm();
    },

    onRefresh: function() {
        var me = this;
        me.lookupReference("grid").getStore().reload();
    },

    onCreate: function() {
        var me = this;
        me.lookupReference("form").getForm().reset();
        me.getViewModel().set("recordId", null);
        me.showForm();
    },

    onCloseForm: function() {
        var me = this;
        me.showGrid();
    },

    onSave: function() {
        var me = this,
            form, data, record, store;
        form = me.lookupReference("form").getForm();
        data = form.getValues();
        store = me.lookupReference("grid").getStore();
        record = me.getViewModel().get("record");
        if(record) {
            // Edit
            record.set(data);
        } else {
            // Create
            record = store.add(data);
        }
        store.sync({
            success: function() {
                me.showGrid();
            },
            failure: function() {
                Ext.Msg.alert("Failed to save");
            }
        });
    },

    onDelete: function() {
        var me = this,
            record, store;
        record = me.getViewModel().get("record");
        store = me.lookupReference("grid").getStore();
        store.remove(record);
        store.sync({
            success: function() {
                me.showGrid();
            },
            failure: function() {
                Ext.Msg.alert("Failed to delete record");
            }
        });
    },

    onInventory: function() {
        var me = this;
        API.Environment.ansible_inventory(
            me.getViewModel().get("selectedEnvironment").get("id"),
            function(result, status) {
                var html = "<pre>" + JSON.stringify(result, undefined, 2) + "</pre>";
                me.lookupReference("inventory").setHtml(html);
                me.getView().getLayout().setActiveItem(2);
            }
        )
    }
});
