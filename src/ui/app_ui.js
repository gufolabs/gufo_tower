import { login_form } from "./login_ui";
import { change_password_form } from "./change_password_ui";
import { desktop } from "./desktop_ui";
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
