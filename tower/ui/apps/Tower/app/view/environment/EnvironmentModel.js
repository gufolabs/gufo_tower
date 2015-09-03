Ext.define('Tower.view.environment.EnvironmentModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.environment-environment',
    data: {
        record: null
    },
    formulas: {
        isNew: function(get) {
            return !!get("record");
        },
        formHeader: function(get) {
            if(!!get("record")) {
                return "Create new environment";
            } else {
                return "Change environment";
            }
        }
    }
});
