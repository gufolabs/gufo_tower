// ----------------------------------------------------------------------
// Environment Form UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { Tower } from "../../lib.js";
import { environment_form_logic } from "./logic.js";

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
                    click: () => { navigation.navigate("/environment"); },
                    width: 32
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: environment_form_logic.on_save
                },
                {
                    view: "button",
                    type: "icon",
                    icon: "trash-o",
                    label: "Delete",
                    autowidth: true,
                    click: environment_form_logic.on_delete
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
                                        validate: Tower.rules.regex(/^[a-zA-Z0-9\-_.]+$/)
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
                                bottomLabel: "Read about that field <a href='https://getnoc.com/config-reference/' target='_'> here</a>",
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
                                        view: "combo",
                                        name: "install_method",
                                        label: "Install method",
                                        width: 250,
                                        required: true,
                                        value: "git",
                                        options: [
                                            { id: "git", value: "Git" }
                                        ]
                                    },
                                    {
                                        view: "text",
                                        name: "playbook_link",
                                        label: "Playbook Repo URL",
                                        required: true,
                                        bottomLabel: "Playbook repo format is <a href=https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support>written here</a>"
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