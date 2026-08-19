// ----------------------------------------------------------------------
// Desktop logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { datacenter_list_logic } from "../datacenter/list/logic.js";
import { environment_list_logic } from "../environment/list/logic.js";
import { environment_form_logic } from "../environment/form/logic.js";
import { environment_inventory_logic } from "../environment/inventory/logic.js";
import { environment_deploy_logic } from "../environment/deploy/logic.js";
import { role_list_logic } from "../role/list/logic.js";
import { role_form_logic } from "../role/form/logic.js";
import { pool_list_logic } from "../pool/list/logic.js";
import { pool_form_logic } from "../pool/form/logic.js";
import { app_logic } from "../app/logic.js";
import { node_list_logic } from "../node/list/logic.js";
import { node_form_logic } from "../node/form/logic.js";
import { service_logic } from "../service/logic.js";
import { settings_logic } from "../settings/logic.js";
import { home_logic } from "../home/logic.js";
import { full_navigation } from "../nav.js";

export class DesktopLogic {
    init = () => {
        home_logic.init();
        environment_list_logic.init();
        environment_form_logic.init();
        environment_inventory_logic.init();
        environment_deploy_logic.init();
        datacenter_list_logic.init();
        role_list_logic.init();
        role_form_logic.init();
        pool_list_logic.init();
        pool_form_logic.init();
        node_list_logic.init();
        node_form_logic.init();
        service_logic.init();
        settings_logic.init();
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