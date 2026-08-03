import { login_form } from "./login_ui.js";
import { change_password_form } from "./change_password_ui.js";
import { desktop } from "./desktop_ui.js";
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
