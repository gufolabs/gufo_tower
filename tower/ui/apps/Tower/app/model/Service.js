Ext.define("Tower.model.Service", {
    extend: "Ext.data.Model",
    requires: [
        "Tower.model.Environment",
        "Tower.model.Pool",
        "Tower.model.Node"
    ],
    fields: [
        {name: "id", type: "string"},
        {
            name: "environment",
            type: "auto"
        },
        {
            name: "pool",
            type: "auto"
        },
        {
            name: "node",
            type: "auto",
            convert: function(value, record) {
                var m;
                if(!value) {
                    return null;
                }
                if(!value.id) {
                    value = {
                        id: value
                    };
                }
                m = Tower.model.Node.create();
                m.set(value);
                return m;
            },
            serialize: function(value, record) {
                if(!value) {
                    return null;
                }
                if(value.id) {
                    return value.id;
                } else {
                    return value;
                }
            }
        },
        {name: "service", type: "string"},
        {name: "n_instances", type: "integer"}
    ]
});
