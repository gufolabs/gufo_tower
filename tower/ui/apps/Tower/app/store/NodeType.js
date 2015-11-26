Ext.define("Tower.store.NodeType", {
    extend: "Ext.data.Store",
    requires: [
        "Ext.data.proxy.Direct"
    ],

    alias: "store.nodetype",
    model: "Tower.model.NodeType",

    proxy: {
        type: "direct",
        paramsAsHash: true,
        batchActions: false,
        api: {
            create: "API.NodeType.create_item",
            read: "API.NodeType.read_items",
            update: "API.NodeType.update_item",
            destroy: "API.NodeType.delete_item"
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
