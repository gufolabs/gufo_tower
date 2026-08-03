export const environment_list = {
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
                    disabled: true,
                    tooltip: "Stop all daemons, update everything, restart everything"
                },
                {
                    view: "multiselect",
                    label: "Deploy options",
                    id: "deployment_options",
                    labelWidth: 100,
                    options: [
                        {
                            id: 1,
                            value: "Install Everything",
                            tooltip: "Ignore other options except verbose. Normal install"
                        },
                        { id: 93, value: "Run pre deploy checks" },
                        { id: 94, value: "Run post deploy tests" },
                        { id: 50, value: "Restart quick", tooltip: "Stop all, start all" },
                        { id: 51, value: "Restart gentle", tooltip: "Restart one by one" },
                        { id: 90, value: "Be verbose", tooltip: "Debug output -v" },
                        { id: 91, value: "Be extremely verbose", tooltip: "Debug output -vvvv" },
                        { id: 92, value: "Show secrets in deploy log", tooltip: "Disable no_log" }
                    ],
                    value: "1,93,94"
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
                    width: 100,
                    sort: "server"
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
            },
            datafetch: Tower.config.datafetch,
            loadahead: Tower.config.loadahead
        }
    ]
};

export const environment_form = {
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
                    width: 32
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
                labelWidth: 130
            },
            scroll: true,
            elements: [
                {
                    view: "text",
                    name: "name",
                    label: "Name",
                    required: true,
                    invalidMessage: "Cannot be empty. You can use following symbols 'a-z,A-Z,0-9,_'",
                    validate: Tower.rules.regex(/^[a-zA-Z0-9_]+$/),
                    value: "NOC"
                },
                {
                    view: "textarea",
                    name: "description",
                    label: "Description",
                    height: 150
                },
                {
                    view: "fieldset",
                    label: "Generic",
                    body: {
                        rows: [
                            {
                                cols: [
                                    {
                                        view: "text",
                                        name: "web_host",
                                        label: "Url",
                                        required: true,
                                        placeholder: "noc.example.com",
                                        bottomLabel: "NOC URL. Prefer DNS than IP",
                                        validate: Tower.rules.regex(/^[a-zA-Z0-9\-_\.]+$/)
                                    },
                                    {
                                        view: "text",
                                        name: "installation_name",
                                        label: "Installation Name",
                                        value: "Unconfigured installation",
                                        required: true
                                    }
                                ]
                            },
                            {
                                view: "combo",
                                name: "env_type",
                                label: "Type",
                                required: true,
                                options: [
                                    { id: "prod", value: "Productive" },
                                    { id: "test", value: "Test" },
                                    { id: "dev", value: "Develop" },
                                    { id: "eval", value: "Evaluation" },
                                    { id: "other", value: "Other" }
                                ],
                                value: "eval"
                            },
                            {
                                placeholder: "yaml:///opt/noc/etc/tower.yml,yaml:///opt/noc/etc/settings.yml,env:///NOC",
                                view: "text",
                                name: "config_order",
                                bottomLabel: "Read about that field <a href='https://kb.nocproject.org/x/8oKYAQ'> here</a>",
                                label: "Config load preference",

                                required: true
                            }
                        ]
                    }
                },
                {
                    view: "fieldset",
                    label: "Repo",
                    body: {
                        rows: [
                            {
                                cols: [
                                    {
                                        view: "label",
                                        label: "",
                                        id: "pulled_label",
                                    }
                                ]
                            },
                            {
                                cols: [
                                    {
                                        view: "text",
                                        name: "playbook_link",
                                        label: "Playbook Repo URL",
                                        required: true,
                                        bottomLabel: "Playbook repo format is <a href=https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support>written here</a>"
                                    },
                                    {
                                        view: "text",
                                        name: "install_method",
                                        label: "Install method",
                                        required: true,
                                        bottomLabel: "Either <strong>git</strong> or custom recommendations",
                                        value: "git"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {}
            ]
        }
    ]
};

export const environment_inventory = {
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
                    click: "environment_logic.show_list",
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
