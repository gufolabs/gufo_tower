// Login form
var change_password_form = {
    id: "change_password_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "button",
                    type: "icon",
                    icon: "arrow-left",
                    click: "desktop_logic.show",
                    width: 32
                },
            ]
        },
        {},  // Top spacer
        {
            cols: [
                {},  // Left spacer
                {
                    rows: [
                        {
                            type: "header",
                            template: "Change tower password"
                        },
                        // Login form
                        {
                            view: "form",
                            id: "change_password_form",
                            width: 350,
                            elementsConfig: {
                                labelWidth: 120
                            },
                            elements: [
                                {
                                    view: "text",
                                    type: "password",
                                    name: "old_password",
                                    label: "Old Password",
                                    placeholder: "Old Password",
                                    required: true,
                                    invalidMessage: "Password cannot be empty"
                                },
                                {
                                    view: "text",
                                    type: "password",
                                    name: "new_password",
                                    label: "New Password",
                                    placeholder: "New Password",
                                    required: true,
                                    invalidMessage: "Password cannot be empty"
                                },
                                {
                                    view: "text",
                                    type: "password",
                                    name: "new_password2",
                                    label: "Retype Password",
                                    placeholder: "Retype new password",
                                    required: true,
                                    invalidMessage: "Password cannot be empty"
                                },
                                //
                                {
                                    cols: [
                                        {
                                            view: "button",
                                            value: "Change",
                                            width: 100,
                                            click: "change_password_logic.on_change_password"
                                        },
                                        {
                                            view: "button",
                                            value: "Reset",
                                            width: 100,
                                            click: "change_password_logic.clear_form"
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
