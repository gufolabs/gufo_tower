// ----------------------------------------------------------------------
// Datacenter logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route, router } from "../../route.js";

export class DatacenterFormLogic {
    init = () => {
    };

    on_route_new = () => {
        $$("datacenter_form_panel").show();
        $$("datacenter_form").setValues({});
    };

    on_route_item = async (dc_id) => {
        try {
            const data = await API.datacenter.get_item({
                id: parseInt(dc_id, 10)
            });
            $$("datacenter_form").setValues(data);
            $$("datacenter_form_panel").show();
        } catch {
            Tower.msg.failed("Failed to get data");
        }
    };

    to_list = () => {
        navigation.navigate("/datacenter");
    };

    on_save = async () => {
        const form = $$("datacenter_form");
        if (!form.validate()) {
            Tower.msg.failed("Error in data");
            return;
        }
        const data = form.getValues();
        try {
            if (data.id === undefined) {
                await API.datacenter.create_item(data);
                this.to_list();
                Tower.msg.complete("Created");
            } else {
                await API.datacenter.update_item(data);
                this.to_list();
                Tower.msg.complete("Changed");
            }
        } catch (err) {
            if (data.id === undefined) {
                Tower.msg.failed("Failed to create " + err);
            } else {
                Tower.msg.failed("Failed to change " + err);
            }
        }
    };

    on_search = (nv, ov) => {
        console.log("Search", nv, ov);
    };

    on_delete = async () => {
        const data = $$("datacenter_form").getValues();

        if (data.id) {
            const confirmed = await webix.confirm({
                title: "Delete datacenter?",
                text: "Are you sure you want to delete this datacenter?<br><br>" +
                    "This operation cannot be undone.",
                type: "confirm-error",
            });

            if (!confirmed) {
                return;
            }
            try {
                await API.datacenter.delete_item(data);
                Tower.msg.complete("Deleted");
                $$("datacenter_list").remove(data.id);
                this.to_list();
            } catch {
                Tower.msg.failed("Failed to delete");
            }
        } else {
            Tower.msg.complete("Deleted");
            this.to_list();
        }
    };
};

export const datacenter_form_logic = new DatacenterFormLogic();

router.push(
    new Route(/^\/datacenter\/new$/, datacenter_form_logic.on_route_new, "datacenter"),
    new Route(/^\/datacenter\/(\d+)$/, datacenter_form_logic.on_route_item, "datacenter")
);
