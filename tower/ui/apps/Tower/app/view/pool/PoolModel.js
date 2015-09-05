Ext.define('Tower.view.pool.PoolModel', {
    extend: 'Ext.app.ViewModel',
    requires: [
        "Tower.store.Pool"
    ],
    alias: 'viewmodel.pool-pool',
    data: {
        record: null
    },
    formulas: {
        isNew: function(get) {
            return !!get("record");
        },
        formHeader: function(get) {
            if(!!get("record")) {
                return "Create new pool";
            } else {
                return "Change pool";
            }
        }
    },
    stores: {
        pools: {
            type: "pool",
            filters: [{
                property: "environment",
                value: "{selectedEnvironment.id}"
            }]
        }
    }
});
