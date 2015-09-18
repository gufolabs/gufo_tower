Ext.define("Tower.store.ServiceNode", {
    extend: "Ext.data.Store",
    alias: "store.servicenode",
    fields: [
        "id",
        "name",
        "datacenter",
        {
            name: "n_instances",
            type: "integer"
        },
        "loglevel"
    ],
    data: []
});
