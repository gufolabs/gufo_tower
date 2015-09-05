Ext.define("Tower.model.Node", {
    extend: "Ext.data.Model",
    fields: [
        {name: "id", type: "string"},
        {
            name: "environment",
            reference: "Tower.model.Environment"
        },
        {
            name: "datacenter",
            reference: "Tower.model.Datacenter"
        },
        {name: "name", type: "string"},
        {name: "description", type: "string"},
        {name: "address", type: "string"},
        {name: "login_as", type: "string"}
    ]
});
