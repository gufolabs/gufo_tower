Ext.define('Tower.view.desktop.DesktopModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.desktop-desktop',
    data: {
        env: ""
    },

    onSelectEnv: function() {
        var me = this;
        console.log("???");
        //console.log(me.getViewModel().data);
    }

    // getEnvironments
    // setEnvironment
});
