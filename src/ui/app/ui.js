// ----------------------------------------------------------------------
// Application ui
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { login_form } from "../login/ui.js";
import { change_password_form } from "../change_password/ui.js";
import { desktop } from "../desktop/ui.js";

export const app_ui = {
    view: "multiview",
    id: "app",
    animate: false,
    cells: [
        login_form,
        change_password_form,
        desktop
    ]
};
