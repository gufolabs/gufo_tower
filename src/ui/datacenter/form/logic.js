// ----------------------------------------------------------------------
// Datacenter logic
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { API } from "../../rpc.js";
import { Tower } from "../../lib.js";
import { Route } from "../../route.js";

export class DatacenterFormLogic {
    init = () => {
    };

    on_route_new = () => {
        $$("datacenter_form_panel").show();
        $$("datacenter_form").setValues({});
    };

    on_route_item = (dc_id) => {
        return API.datacenter.get_item({ id: parseInt(dc_id, 10) }).then((data) => {
            $$("datacenter_form").setValues(data);
            $$("datacenter_form_panel").show();
        }, (err) => {
            Tower.msg.failed("Failed to get data");
        });
    };

    on_save = () => {
        let data;
        const form = $$("datacenter_form");

        if (form.validate()) {
            data = form.getValues();
            if (data.id === undefined) {
                API.datacenter.create_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        navigation.navigate("/datacenter");
                        Tower.msg.complete("Created");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to create " + err);
                    }
                );
            } else {
                API.datacenter.update_item(data).then(
                    function (result) {
                        form.setValues(result);
                        form.save();
                        navigation.navigate("/datacenter");
                        Tower.msg.complete("Changed");
                    },
                    function (err) {
                        Tower.msg.failed("Failed to change " + err);
                    }
                );
            }
        } else {
            Tower.msg.failed("Error in data");
        }
    };

    on_search = (nv, ov) => {
        console.log("Search", nv, ov);
    };

    on_delete = () => {
        const data = $$("datacenter_form").getValues();
        if (data.id) {
            API.datacenter.delete_item(data).then(
                function () {
                    Tower.msg.complete("Deleted");
                    $$("datacenter_list").remove(data.id);
                    navigation.navigate("/datacenter");
                },
                function () {
                    Tower.msg.failed("Failed to delete");
                }
            );
        } else {
            Tower.msg.complete("Deleted");
            navigation.navigate("/datacenter");
        }
    };
};

export const datacenter_form_logic = new DatacenterFormLogic();

export const datacenter_form_routes = [
    new Route(/^\/datacenter\/new$/, datacenter_form_logic.on_route_new, "datacenter"),
    new Route(/^\/datacenter\/(\d+)$/, datacenter_form_logic.on_route_item, "datacenter"),
];
