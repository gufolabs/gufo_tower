Ext.define('Tower.view.datacenter.DatacenterModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.datacenter-datacenter',
    data: {
        record: null
    },
    formulas: {
        isNew: function(get) {
            return !!get("record");
        },
        formHeader: function(get) {
            if(!!get("record")) {
                return "Create new datacenter";
            } else {
                return "Change datacenter";
            }
        }
    }
});
