Ext.define("Tower.view.service.List", {
    extend: "Ext.grid.Panel",
    requires: [
        "Ext.form.field.ComboBox",
        "Ext.form.field.Number",
        "Ext.grid.plugin.CellEditing",
        "Tower.store.ServicePool",
        "Tower.store.ServiceService",
        "Tower.store.ServiceNode"
    ],
    xtype: "app-service-list",
    reference: "grid",

    bind: "{services}",
    autoLoad: true,
    columns: [
        {
            text: "Node",
            dataIndex: "name",
            width: 100
        },
        {
            text: "Datacenter",
            dataIndex: "datacenter",
            width: 100
        },
        {
            text: "Instances",
            dataIndex: "n_instances",
            width: 100,
            align: "right",
            editor: {
                xtype: "numberfield",
                allowBlank: false,
                minValue: 0
            },
            renderer: function (v) {
                switch (v) {
                    case 0:
                        return "<i class='x-fa fa-times'></i>";
                    case 1:
                        return "<i class='x-fa fa-check'></i>";
                    default:
                        return "" + v;
                }
            }
        },
        {
            text: "Loglevel",
            dataIndex: "loglevel",
            width: 100,
            editor: {
                xtype: "combobox",
                allowBlank: false,
                store: [
                    "notset",
                    "debug",
                    "info",
                    "warning",
                    "error",
                    "critical"
                ]
            }
        }
    ],
    store: {
        type: "servicenode"
    },
    plugins: [{
        ptype: "cellediting",
        clicksToEdit: 1
    }],
    viewConfig: {
        emptyText: "Select pool and service"
    },
    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            items: [
                {
                    xtype: "button",
                    text: "Save",
                    iconCls: "x-fa fa-save",
                    disabled: true,
                    reference: "saveButton",
                    handler: "onSave"
                },
                "-",
                {
                    xtype: "combobox",
                    name: "pool",
                    fieldLabel: "Pool",
                    valueField: "id",
                    displayField: "name",
                    labelWidth: 50,
                    reference: "poolsCombo",
                    store: {
                        type: "servicepool"
                    },
                    queryMode: "local",
                    autoSelect: true,
                    listeners: {
                        select: "onSelect"
                    }
                },
                {
                    xtype: "combobox",
                    name: "service",
                    fieldLabel: "Service",
                    valueField: "id",
                    displayField: "name",
                    labelWidth: 50,
                    reference: "servicesCombo",
                    store: {
                        type: "serviceservice"
                    },
                    queryMode: "local",
                    autoSelect: true,
                    listeners: {
                        select: "onSelect"
                    }
                },
                "-",
                {
                    xtype: "button",
                    text: "Summary",
                    iconCls: "x-fa fa-table",
                    handler: "onShowPivot"
                }
            ]
        }
    ],
    listeners: {
        edit: "onServiceEdit"
    }
});
