Ext.define('Tower.view.environment.EnvironmentModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.environment-environment',
    data: {
        record: null,
        deployStatus: false,
        nOk: 0,
        nChanged: 0,
        nUnreachable: 0,
        nFailed: 0
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
        },
        deployText: function(get) {
            if(get("deployStatus")) {
                return "Complete";
            } else {
                return "Running";
            }
        }
    }
});
