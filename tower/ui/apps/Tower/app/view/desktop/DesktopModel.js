Ext.define('Tower.view.desktop.DesktopModel', {
    extend: 'Ext.app.ViewModel',
    requires: [
        "Tower.model.Environment"
    ],
    alias: 'viewmodel.desktop-desktop',
    stores: {
        environments: {
            type: "environment",
            autoLoad: true
        }
    },
    data: {
        selectedEnvironment: null
    },
    formulas: {
        isEnvironmentSelected: function(get) {
            return !!get("selectedEnvironment");
        },

        environmentHeader: function(get) {
            var se = get("selectedEnvironment");
            if(!se) {
                return "(Select Environment)";
            } else {
                return se.get("name");
            }
        }
    }
});
