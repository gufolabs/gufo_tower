Ext.define("Tower.model.Node", {
    extend: "Ext.data.Model",
    requires: [
        "Tower.model.Environment",
        "Tower.model.Datacenter"
    ],
    fields: [
        {name: "id", type: "string"},
        {
            name: "environment",
            type: "auto"
        },
        {
            name: "datacenter",
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
                m = Tower.model.Datacenter.create();
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
        {name: "name", type: "string"},
        {name: "description", type: "string"},
        {name: "address", type: "string"},
        {name: "login_as", type: "string"}
    ]
});
