Ext.define("Tower.store.Environment", {
    extend: "Ext.data.Store",
    requires: [
        "Ext.data.proxy.Direct"
    ],

    alias: "store.environment",

    fields: [
        {name: "id", type: "string"},
        {name: "name", type: "string"},
        {name: "description", type: "string"},
        {name: "env_type", type: "string"},
        {name: "sys_user", type: "string"},
        {name: "sys_group", type: "string"},
        {name: "sys_prefix", type: "string"},
        {name: "repo", type: "string"},
        {name: "branch", type: "string"},
        {name: "pg_db", type: "string"},
        {name: "pg_user", type: "string"},
        {name: "pg_password", type: "string"},
        {name: "mongo_db", type: "string"},
        {name: "mongo_user", type: "string"},
        {name: "mongo_password", type: "string"},
        {name: "mongo_rs", type: "string"},
        {name: "mongo_engine", type: "string"}
    ],

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
