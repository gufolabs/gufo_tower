// ----------------------------------------------------------------------
// Login UI
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { login_logic } from "./logic.js";
// Login form
export const login_form = {
    id: "login_panel",
    rows: [
        {},  // Top spacer
        {
            cols: [
                {},  // Left spacer
                {
                    id: "login",
                    rows: [
                        {
                            type: "header",
                            template: "Gufo Tower Login"
                        },
                        // Login form
                        {
                            view: "form",
                            id: "login_form",
                            width: 300,
                            elementsConfig: {
                                labelWidth: 80
                            },
                            elements: [
                                {
                                    view: "text",
                                    name: "user",
                                    id: "user",
                                    placeholder: "Username",
                                    label: "User",
                                    required: true,
                                    invalidMessage: "User name cannot be empty"
                                },
                                {
                                    view: "text",
                                    type: "password",
                                    name: "password",
                                    id: "password",
                                    label: "Password",
                                    placeholder: "Password",
                                    required: true,
                                    invalidMessage: "Password cannot be empty"
                                },
                                //
                                {
                                    cols: [
                                        {
                                            view: "button",
                                            value: "Login",
                                            width: 100,
                                            click: login_logic.on_login,
                                            hotkey: "enter"
                                        },
                                        {
                                            view: "button",
                                            value: "Reset",
                                            width: 100,
                                            click: login_logic.clear_form
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {}  // Right spacer
            ]
        },
        {}  // Bottom spacer
    ]
};
