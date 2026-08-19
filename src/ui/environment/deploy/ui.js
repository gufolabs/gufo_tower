// ----------------------------------------------------------------------
// Environment Deploy UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
export const environment_deploy = {
    id: "environment_deploy_panel",
    rows: [
        {
            view: "toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: () => { navigation.navigate("../.."); },
                    width: 32
                },
                {
                    view: "template",
                    id: "environment_deploy_badges",
                    type: "header",
                    borderless: true,
                    template: "<span class='ansible-ok-tag' title='ok'>#ok#</span> " +
                        "<span class='ansible-changed-tag' title='changed'>#changed#</span> " +
                        "<span class='ansible-unreachable-tag' title='unreachable'>#unreach#</span> " +
                        "<span class='ansible-failed-tag' title='failed'>#failed#</span> " +
                        "Deploy: #status#",
                    data: {
                        ok: 0,
                        changed: 0,
                        unreach: 0,
                        failed: 0,
                        status: "Waiting"
                    }
                },
                {},
                {
                    view: "template",
                    id: "environment_deploy_clock",
                    type: "header",
                    align: "right",
                    width: 70,
                    borderless: true,
                    template: "#time#",
                    data: {
                        time: "00:00"
                    }
                }
            ]
        },
        {
            view: "template",
            id: "environment_deploy_output",
            template: "Deploy",
            scroll: true,
            css: "deploy_log"
        }
    ]
};
