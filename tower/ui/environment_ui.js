var environment_list = {
    id: "environment_list_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "search",
                    placeholder: "Search...",
                    width: 150,
                    on: {
                        "onChange": "environment_logic.on_search"
                    }
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "plus",
                    autowidth: true,
                    label: "Create new...",
                    click: "environment_logic.on_add"
                },
                {
                    view: "button",
                    id: "environment_inventory_button",
                    type: "icon",
                    icon: "search",
                    label: "Inventory",
                    click: "environment_logic.on_show_inventory",
                    autowidth: true,
                    disabled: true
                },
                {
                    view: "button",
                    id: "environment_pull_button",
                    type: "icon",
                    icon: "arrow-circle-down",
                    label: "Pull",
                    click: "environment_logic.on_pull",
                    autowidth: true,
                    disabled: true
                },
                {
                    view: "button",
                    id: "environment_deploy_button",
                    type: "icon",
                    icon: "play",
                    label: "Deploy",
                    click: "environment_logic.on_deploy",
                    autowidth: true,
                    disabled: true
                }

            ]
        },
        {
            view: "datatable",
            id: "environment_list",
            select: "row",
            columns: [
                {
                    id: "name",
                    header: "Environment",
                    width: 100
                },
                {
                    id: "env_type",
                    header: "Type",
                    width: 120
                },
                {
                    id: "web_host",
                    header: "URL",
                    width: 150,
                    format: function (v) {
                        return "<a target='_' href='https://" + v + "/'>" + v + "</a>";
                    }
                },
                {
                    id: "description",
                    header: "Description",
                    fillspace: true
                }
            ],
            on: {
                onSelectChange: "environment_logic.on_select",
                onItemDblClick: "environment_logic.on_edit"
            }
        }
    ]
};

var environment_form = {
    id: "environment_form_panel",
    rows: [
        {
            view: "toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: "environment_logic.show_list",
                    width: 20
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: "environment_logic.on_save"
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: "environment_logic.on_delete"
                },
                {}
            ]
        },
        {
            view: "form",
            id: "environment_form",
            elementsConfig: {
                labelWidth: 110
            },
            scroll: true,
            elements: [
                {
                    view: "text",
                    name: "name",
                    label: "Name",
                    required: true,
                    placeholder: "Environment name",
                    invalidMessage: "Cannot be empty"
                },
                {
                    view: "textarea",
                    name: "description",
                    label: "Description",
                    height: 150
                },
                {
                    view: "combo",
                    name: "env_type",
                    label: "Type",
                    required: true,
                    options: [
                        {id: "prod", value: "Productive"},
                        {id: "test", value: "Test"},
                        {id: "dev", value: "Develop"},
                        {id: "eval", value: "Evaluation"},
                        {id: "other", value: "Other"}
                    ],
                    value: "eval"
                },
                {
                    view: "fieldset",
                    label: "Repo",
                    body: {
                        cols: [
                            {
                                view: "text",
                                name: "repo",
                                label: "Repo URL",
                                required: true,
                                value: "https://bitbucket.com/nocproject/noc"
                            },
                            {
                                view: "text",
                                name: "branch",
                                label: "Branch",
                                required: true,
                                value: "feature/microservices"
                            },
                            {
                                view: "text",
                                name: "changeset",
                                required: true,
                                label: "Changeset",
                                value: "tip"
                            }
                        ]
                    }
                },
                {
                    view: "fieldset",
                    label: "Web",
                    body: {
                        cols: [
                            {
                                view: "text",
                                name: "web_host",
                                label: "Host",
                                value: "noc.example.com",
                                required: true
                            },
                            {
                                view: "text",
                                name: "installation_name",
                                label: "Installation Name",
                                value: "Unconfigured installation",
                                required: true
                            },
                            {
                                view: "textarea",
                                name: "cert",
                                label: "SSL Cert + Key",
                                placeholder: "Copy&Paste private key, certificate and all intermediate certificates in PEM format"
                            }
                        ]
                    }
                },
                {
                    view: "fieldset",
                    label: "System",
                    body: {
                        cols: [
                            {
                                view: "text",
                                name: "sys_user",
                                label: "User",
                                value: "noc",
                                required: true
                            },
                            {
                                view: "text",
                                name: "sys_group",
                                label: "Group",
                                value: "noc",
                                required: true
                            },
                            {
                                view: "text",
                                name: "sys_prefix",
                                label: "Prefix",
                                value: "/opt/noc",
                                required: true
                            }
                        ]
                    }
                },
                {
                    view: "fieldset",
                    label: "PostgreSQL",
                    body: {
                        cols: [
                            {
                                view: "text",
                                name: "pg_db",
                                label: "Database",
                                value: "noc",
                                required: true
                            },
                            {
                                view: "text",
                                name: "pg_user",
                                label: "User",
                                value: "noc",
                                required: true
                            },
                            {
                                view: "text",
                                type: "password",
                                name: "pg_password",
                                label: "Password",
                                value: "noc",
                                required: true
                            }
                        ]
                    }
                },
                {
                    view: "fieldset",
                    label: "MongoDB",
                    body: {
                        cols: [
                            {
                                view: "text",
                                name: "mongo_db",
                                label: "Database",
                                value: "noc",
                                required: true
                            },
                            {
                                view: "combo",
                                name: "mongo_engine",
                                label: "Storage Engine",
                                options: [
                                    {
                                        id: "wiredTiger",
                                        value: "Wired Tiger"
                                    },
                                    {id: "mmapv1", value: "MMAPv1"}
                                ],
                                value: "wiredTiger",
                                required: true
                            },
                            {
                                view: "text",
                                name: "mongo_rs",
                                label: "Replica Set",
                                value: "noc",
                                required: true
                            },
                            {
                                view: "text",
                                name: "mongo_user",
                                label: "User",
                                value: "noc",
                                required: true
                            },
                            {
                                view: "text",
                                type: "password",
                                name: "mongo_password",
                                label: "Password",
                                value: "noc",
                                inputType: "password",
                                required: true
                            }
                        ]
                    }
                },
                {}
            ]
        }
    ]
};

var environment_inventory = {
    id: "environment_inventory_panel",
    rows: [
        {
            view: "toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: "environment_logic.show_list",
                    width: 32
                },
                {
                    view: "label",
                    label: "Ansible Inventory"
                },
                {}
            ]
        },
        {
            view: "template",
            id: "environment_inventory_text",
            template: "<pre>#text#</pre>",
            data: {
                text: "?"
            },
            scroll: true
        }
    ]
};

var environment_deploy = {
    id: "environment_deploy_panel",
    rows: [
        {
            view: "toolbar",
            cols: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: "environment_logic.show_list",
                    width: 20
                },
                {
                    view: "template",
                    id: "environment_deploy_badges",
                    type: "header",
                    borderless: true,
                    template:
                        "<span class='ansible-ok-tag' title='ok'>#ok#</span> " +
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
