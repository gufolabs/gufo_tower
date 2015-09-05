Ext.define("Tower.store.Environment", {
    extend: "Ext.data.Store",
    requires: [
        "Ext.data.proxy.Direct"
    ],

    alias: "store.environment",
    model: "Tower.model.Environment",

    proxy: {
        type: "direct",
        paramsAsHash: true,
        batchActions: false,
        api: {
            create: "API.Environment.create_item",
            read: "API.Environment.read_items",
            update: "API.Environment.update_item",
            destroy: "API.Environment.delete_item"
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
