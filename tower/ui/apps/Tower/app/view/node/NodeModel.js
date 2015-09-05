Ext.define('Tower.view.node.NodeModel', {
    extend: 'Ext.app.ViewModel',
    requires: [
        "Tower.store.Node"
    ],
    alias: 'viewmodel.node-node',
    data: {
        record: null
    },
    formulas: {
        isNew: function(get) {
            return !!get("record");
        },
        formHeader: function(get) {
            if(!!get("record")) {
                return "Create new node";
            } else {
                return "Change node";
            }
        }
    },
    stores: {
        nodes: {
            type: "node",
            filters: [{
                property: "environment",
                value: "{selectedEnvironment.id}"
            }]
        }
    }
});
