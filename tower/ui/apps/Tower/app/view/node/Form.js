Ext.define("Tower.view.node.Form", {
    extend: "Ext.form.Panel",
    xtype: "app-node-form",
    reference: "form",
    autoScroll: true,

    requires: [
        "Ext.form.field.Text",
        "Ext.form.field.TextArea",
        "Ext.form.field.ComboBox",
        "Ext.form.FieldSet",
        "Tower.store.Datacenter",
        "Tower.store.NodeType"
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
            regex: /^[a-zA-Z][a-zA-Z0-9\-_]*$/
        },
        {
            name: "datacenter",
            xtype: "combobox",
            store: {
                type: "datacenter"
            },
            fieldLabel: "Datacenter",
            valueField: "id",
            displayField: "name",
            allowBlank: false
        },
        {
            name: "description",
            xtype: "textarea",
            fieldLabel: "Description",
            allowBlank: true,
            anchor: "100%"
        },
        {
            xtype: "fieldset",
            title: "Connect",
            layout: "hbox",
            defaults: {
                labelAlign: "top",
                padding: "0 2 0 0"
            },
            items: [
                {
                    name: "node_type",
                    xtype: "combobox",
                    store: {
                        type: "nodetype"
                    },
                    fieldLabel: "Node Type",
                    valueField: "id",
                    displayField: "name",
                    allowBlank: false
                },
                {
                    name: "address",
                    xtype: "textfield",
                    fieldLabel: "Address"
                },
                {
                    name: "login_as",
                    xtype: "textfield",
                    fieldLabel: "Login As"
                }
            ]
        }
    ]
});
