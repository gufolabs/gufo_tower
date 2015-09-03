Ext.define("Tower.view.datacenter.Form", {
    extend: "Ext.form.Panel",
    xtype: "app-datacenter-form",
    reference: "form",
    autoScroll: true,

    requires: [
        "Ext.form.field.Text",
        "Ext.form.field.TextArea"
    ],

    header: {
        bind: {
            html: "{formHeader}"
        }
    },

    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            items: [
                {
                    iconCls: "x-fa fa-arrow-left",
                    handler: "onCloseForm"
                },
                "-",
                {
                    iconCls: "x-fa fa-floppy-o",
                    text: "Save",
                    formBind: true,
                    handler: "onSave"
                },
                "-",
                {
                    iconCls: "x-fa fa-trash-o",
                    text: "Delete",
                    bind: {
                        disabled: "{!isNew}"
                    },
                    handler: "onDelete"
                }
            ]
        }
    ],

    items: [
        {
            name: "name",
            xtype: "textfield",
            fieldLabel: "Name",
            allowBlank: false,
            regex: /^[a-zA-Z][a-zA-Z0-9]*$/
        },
        {
            name: "description",
            xtype: "textarea",
            fieldLabel: "Description",
            allowBlank: true,
            anchor: "100%"
        }
    ]
});
