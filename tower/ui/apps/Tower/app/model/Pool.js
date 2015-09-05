Ext.define("Tower.model.Pool", {
    extend: "Ext.data.Model",
    fields: [
        {name: "id", type: "string"},
        {
            name: "environment",
            reference: "Tower.model.Environment"
        },
        {name: "name", type: "string"},
        {name: "description", type: "string"}
    ]
});
