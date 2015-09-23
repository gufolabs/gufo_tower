Ext.define("Tower.view.environment.Deploy", {
    extend: "Ext.panel.Panel",
    xtype: "app-environment-deploy",
    requires: [
        "Tower.store.Environment"
    ],
    reference: "deploy",
    dockedItems: [
        {
            xtype: "toolbar",
            dock: "top",
            items: [
                {
                    iconCls: "x-fa fa-arrow-left",
                    handler: "onCloseForm"
                }
            ]
        }
    ],
    header: {
        bind: {
            html: "Deploy: {deployText} " +
                  "<span class='ansible-ok-tag' title='ok'>{nOk}</span> " +
                  "<span class='ansible-changed-tag' title='changed'>{nChanged}</span> " +
                  "<span class='ansible-unreachable-tag' title='unreachable'>{nUnreachable}</span> " +
                  "<span class='ansible-failed-tag' title='failed'>{nFailed}</span>"
        }
    },
    autoScroll: true,
    bodyCls: "deploy-log"
});
