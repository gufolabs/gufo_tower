// ----------------------------------------------------------------------
// Environment Deploy Form UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import { deploy_options, on_deploy } from "../../../state.js";

const set_option = (id, value) => {
    if (value) {
        deploy_options.add(id);
    } else {
        deploy_options.delete(id);
    }
};

const set_radio_option = (ids, value) => {
    for (const id of ids) {
        deploy_options.delete(id);
    }
    if (value) {
        deploy_options.add(Number(value));
    }
};

export const environment_deploy_form = {
    view: "window",
    id: "environment_deploy_form",
    modal: true,
    position: "center",
    width: 500,
    head: "Run Deploy",
    body: {
        view: "form",
        id: "environment_deploy_form_form",
        elements: [
            {
                view: "fieldset",
                label: "Installation",
                body: {
                    rows: [
                        {
                            view: "checkbox",
                            id: "environment_deploy_install_everything",
                            labelRight: "Install Everything",
                            labelWidth: 0,
                            name: "install_everything",
                            value: 1,
                            on: {
                                onChange: function (value) {
                                    set_option(1, value);
                                }
                            }
                        }
                    ]
                }
            },
            {
                view: "fieldset",
                label: "Checks",
                body: {
                    rows: [
                        {
                            view: "checkbox",
                            id: "environment_deploy_pre_deploy",
                            labelRight: "Run pre deploy checks",
                            labelWidth: 0,
                            name: "pre_deploy",
                            value: 1,
                            on: {
                                onChange: function (value) {
                                    set_option(93, value);
                                }
                            }
                        },
                        {
                            view: "checkbox",
                            id: "environment_deploy_post_deploy",
                            labelRight: "Run post deploy tests",
                            labelWidth: 0,
                            name: "post_deploy",
                            value: 1,
                            on: {
                                onChange: function (value) {
                                    set_option(94, value);
                                }
                            }
                        }
                    ]
                }
            },
            {
                view: "fieldset",
                label: "Restart",
                body: {
                    rows: [
                        {
                            view: "radio",
                            id: "environment_deploy_restart",
                            name: "restart",
                            value: 0,
                            options: [
                                { id: 0, value: "No restart" },
                                { id: 50, value: "Quick" },
                                { id: 51, value: "Gentle" }
                            ],
                            on: {
                                onChange: function (value) {
                                    set_radio_option([50, 51], value);
                                }
                            }
                        }
                    ]
                }
            },
            {
                view: "fieldset",
                label: "Output",
                body: {
                    rows: [
                        {
                            view: "radio",
                            id: "environment_deploy_output_level",
                            name: "output_level",
                            value: 0,
                            options: [
                                { id: 0, value: "Normal" },
                                { id: 90, value: "Verbose" },
                                { id: 91, value: "Extremely verbose" }
                            ],
                            on: {
                                onChange: function (value) {
                                    set_radio_option([90, 91], value);
                                }
                            }
                        },
                        {
                            view: "checkbox",
                            id: "environment_deploy_show_secrets",
                            labelRight: "Show secrets in deploy log",
                            labelWidth: 0,
                            name: "show_secrets",
                            value: 0,
                            on: {
                                onChange: function (value) {
                                    set_option(92, value);
                                }
                            }
                        }
                    ]
                }
            },
            {
                cols: [
                    {},
                    {
                        view: "button",
                        label: "Cancel",
                        width: 100,
                        click: function () {
                            this.getTopParentView().hide();
                            navigation.navigate("/environment");
                        }
                    },
                    {
                        view: "button",
                        label: "Deploy",
                        type: "form",
                        width: 100,
                        id: "environment_deploy_submit",
                        click: function () {
                            this.getTopParentView().hide();
                            on_deploy.fire();
                        }
                    }
                ]
            }
        ]
    },
    on: {
        onShow: function () {
            const state = deploy_options.state;
            $$("environment_deploy_install_everything").setValue(
                state.has(1)
            );
            $$("environment_deploy_pre_deploy").setValue(
                state.has(93)
            );
            $$("environment_deploy_post_deploy").setValue(
                state.has(94)
            );
            $$("environment_deploy_restart").setValue(
                state.has(50) ? 50 :
                    state.has(51) ? 51 : 0
            );
            $$("environment_deploy_output_level").setValue(
                state.has(91) ? 91 :
                    state.has(90) ? 90 : 0
            );
            $$("environment_deploy_show_secrets").setValue(
                state.has(92)
            );
        }
    }
};