Ext.define("Tower.store.Datacenter", {
    extend: "Ext.data.Store",
    requires: [
        "Ext.data.proxy.Direct"
    ],

    alias: "store.datacenter",

    fields: [
        {name: "id", type: "string"},
        {name: "name", type: "string"},
        {name: "description", type: "string"}
    ],

    proxy: {
        type: "direct",
        paramsAsHash: true,
        batchActions: false,
        api: {
            create: "API.Datacenter.create_item",
            read: "API.Datacenter.read_items",
            update: "API.Datacenter.update_item",
            destroy: "API.Datacenter.delete_item"
        },
        reader: {
            type: "json",
            rootProperty: "data",
            successProperty: "success",
            totalProperty: "total"
        },
        limitParam: "limit",
        pageParam: "page"
    },

    remoteFilter: true,
    remoteSort: true
});
