Ext.define("Tower.view.environment.Form", {
    extend: "Ext.form.Panel",
    xtype: "app-environment-form",
    reference: "form",
    autoScroll: true,

    requires: [
        "Ext.form.field.Text",
        "Ext.form.field.TextArea",
        "Ext.form.field.ComboBox",
        "Ext.form.FieldSet"
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
        },
        {
            name: "env_type",
            xtype: "combobox",
            fieldLabel: "Type",
            allowBlank: false,
            store: [
                ["prod", "Productive"],
                ["test", "Test"],
                ["dev", "Develop"],
                ["eval", "Evaluation"],
                ["other", "Other"]
            ],
            value: "eval"
        },
        {
            xtype: "fieldset",
            title: "Repo",
            layout: "hbox",
            defaults: {
                labelAlign: "top"
            },
            items: [
                {
                    name: "repo",
                    xtype: "textfield",
                    fieldLabel: "Repo URL",
                    value: "https://bitbucket.com/nocproject/noc",
                    width: 300
                },
                {
                    name: "branch",
                    xtype: "textfield",
                    fieldLabel: "Branch",
                    value: "default",
                    width: 200
                },
                {
                    name: "changeset",
                    xtype: "textfield",
                    fieldLabel: "Changeset",
                    value: "tip",
                    width: 200
                }
            ]
        },
        {
            xtype: "fieldset",
            title: "Web",
            layout: "hbox",
            defaults: {
                labelAlign: "top",
                padding: "0 2 0 0"
            },
            items: [
                {
                    name: "web_host",
                    xtype: "textfield",
                    fieldLabel: "Host",
                    value: "127.0.0.1:8000",
                    width: 200
                }
            ]
        },
        {
            xtype: "fieldset",
            title: "System",
            layout: "hbox",
            defaults: {
                labelAlign: "top",
                padding: "0 2 0 0"
            },
            items: [
                {
                    name: "sys_user",
                    xtype: "textfield",
                    fieldLabel: "User",
                    value: "noc",
                    width: 100
                },
                {
                    name: "sys_group",
                    xtype: "textfield",
                    fieldLabel: "Group",
                    value: "noc",
                    width: 100
                },
                {
                    name: "sys_prefix",
                    xtype: "textfield",
                    fieldLabel: "Prefix",
                    value: "/opt/noc",
                    width: 200
                }
            ]
        },
        {
            xtype: "fieldset",
            title: "PostgreSQL",
            layout: "hbox",
            defaults: {
                labelAlign: "top",
                padding: "0 2 0 0"
            },
            items: [
                {
                    name: "pg_db",
                    xtype: "textfield",
                    fieldLabel: "Database",
                    value: "noc",
                    width: 100
                },
                {
                    name: "pg_user",
                    xtype: "textfield",
                    fieldLabel: "User",
                    value: "noc",
                    width: 100
                },
                {
                    name: "pg_password",
                    xtype: "textfield",
                    fieldLabel: "Password",
                    value: "noc",
                    width: 100,
                    inputType: "password"
                }
            ]
        },
        {
            xtype: "fieldset",
            title: "MongoDB",
            layout: "hbox",
            defaults: {
                labelAlign: "top",
                padding: "0 2 0 0"
            },
            items: [
                {
                    name: "mongo_db",
                    xtype: "textfield",
                    fieldLabel: "Database",
                    value: "noc",
                    width: 100
                },
                {
                    name: "mongo_engine",
                    xtype: "combobox",
                    fieldLabel: "Storage Engine",
                    store: [
                        ["wiredTiger", "Wired Tiger"],
                        ["mmapv1", "MMAPv1"]
                    ],
                    value: "wiredTiger",
                    width: 150
                },
                {
                    name: "mongo_rs",
                    xtype: "textfield",
                    fieldLabel: "Replica Set",
                    value: "noc",
                    width: 100
                },
                {
                    name: "mongo_user",
                    xtype: "textfield",
                    fieldLabel: "User",
                    value: "noc",
                    width: 100
                },
                {
                    name: "mongo_password",
                    xtype: "textfield",
                    fieldLabel: "Password",
                    value: "noc",
                    width: 200,
                    inputType: "password"
                }
            ]
        }
    ]
});
