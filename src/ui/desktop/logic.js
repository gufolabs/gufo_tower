// ----------------------------------------------------------------------
// Desktop logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { environment_list_logic } from "../environment/list/logic.js";
import { app_logic } from "../app/logic.js";
import { full_navigation } from "../nav.js";

export class DesktopLogic {
    init = () => {
        environment_list_logic.init();
    };

    show = () => {
        $$("desktop").show();
    };

    on_select_app = (selection) => {
        const item = $$("sidebar").getItem(selection[0]);
        navigation.navigate(item.path);
    };

    select_environment = (env) => {
        $$("environment_label").setValue("Gufo Tower: " + env.name);
        const sidebar = $$("sidebar");
        const items = full_navigation.map((item) => ({
            ...item,
            path: item.path.replaceAll(":id", env.id),
        }));
        sidebar.clearAll();
        sidebar.parse(items);
    };

    on_menu_click = (item_id) => {
        switch (item_id) {
            case "docs":
                window.open("/docs/index.html", "_blank");
                break;
            case "logout":
                app_logic.logout();
                break;
            case "change_password":
                navigation.navigate("/change-password");
                break;
            default:
                break;
        }
    };
};
export const desktop_logic = new DesktopLogic();