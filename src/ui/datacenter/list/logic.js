// ----------------------------------------------------------------------
// Datacenter logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { Route, router } from "../../route.js";

export class DatacenterListLogic {
    on_route = () => {
        $$("datacenter_list_panel").show();
        datacenter_list_logic.load();
    };

    // Load data info list
    load = () => {
        $$("datacenter_list").load("rpc->datacenter");
    };

    on_search = (nv, ov) => {
        console.log("Search", nv, ov);
    };
};

export const datacenter_list_logic = new DatacenterListLogic();

router.push(
    new Route(/^\/datacenter$/, datacenter_list_logic.on_route, "datacenter")
);