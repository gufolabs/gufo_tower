// ----------------------------------------------------------------------
// Desktop logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { environment_list_logic } from "../environment/list/logic.js";
import { full_navigation } from "../nav.js";
import { current_env, installation_name } from "../state.js";
import { Tower } from "../lib.js";
import { API } from "../rpc.js";

export class DesktopLogic {
    init = () => {
        environment_list_logic.init();
        current_env.subscribe(() => {
            this.update_title();
            this.update_menu();
        });
        installation_name.subscribe(() => { this.update_title(); });
    };

    show = () => {
        $$("desktop").show();
    };

    on_select_app = (selection) => {
        const item = $$("sidebar").getItem(selection[0]);
        navigation.navigate(item.path);
    };

    update_title = () => {
        const name = current_env.state === null ?
            installation_name.state
            : `${installation_name.state} / ${current_env.state.name}`;
        $$("environment_label").setValue(`Gufo Tower / ${name}`);
    }

    update_menu = () => {
        if (current_env.state === null) {
            return;
        }
        const sidebar = $$("sidebar");
        const env_id = current_env.state.id;
        const items = full_navigation.map((item) => ({
            ...item,
            path: item.path.replaceAll(":id", env_id),
        }));
        sidebar.clearAll();
        sidebar.parse(items);
    }

    on_menu_click = async (item_id) => {
        switch (item_id) {
            case "docs":
                window.open("/docs/index.html", "_blank");
                break;
            case "logout":
                await this.logout();
                break;
            case "change_password":
                navigation.navigate("/change-password");
                break;
            default:
                break;
        }
    };

    logout = async () => {
        try {
            await API.login.logout();
            navigation.navigate("/login");
            Tower.msg.complete("Logged out");
        } catch {
            Tower.msg.failed("Failed to log out");
        }
    };
};
export const desktop_logic = new DesktopLogic();