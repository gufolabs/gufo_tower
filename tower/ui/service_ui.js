var service_panel = {
    id: "service_panel",
    rows: [
        {
            view: "toolbar",
            elements: [
                {
                    view: "button",
                    type: "icon",
                    icon: "save",
                    label: "Save",
                    autowidth: true,
                    click: "service_logic.on_save"
                }
            ]
        },
        {
            cols: [
                {
                    view: "grouplist",
                    id: "service_list",
                    width: 170,
                    scroll: true,
                    select: true,
                    navigation: true,
                    templateItem: "<i class='fa fa-#icon#'></i> #value# <span class='webix_badge' style='background-color: green !important;'>#n_backup_instances#</span><span class='webix_badge'>#n_instances#</span>",
                    on: {
                        "onSelectChange": "service_logic.on_select_service"
                    }
                },
                {
                    view: "datatable",
                    id: "service_nodes_list",
                    select: "row",
                    editable: true,
                    fillspace: true,
                    scroll: true,
                    width: 400,
                    columns: [
                        {
                            id: "datacenter",
                            header: "Datacenter",
                            width: 100
                        },
                        {
                            id: "node",
                            header: "Node",
                            width: 100
                        },
                        {
                            id: "n_instances",
                            header: "Instances",
                            editor: "text",
                            format: function (value) {
                                if (typeof value === "string") {
                                    value = parseInt(value);
                                }
                                switch (value) {
                                    case 0:
                                        return "<i class='fa fa-times'></i>";
                                    case 1:
                                        return "<i class='fa fa-check'></i>";
                                    default:
                                        return value;
                                }
                            },
                            width: 100
                        },
                        {
                            id: "n_backup_instances",
                            header: "Backup",
                            editor: "text",
                            format: function (value) {
                                if (typeof value === "string") {
                                    value = parseInt(value);
                                }
                                switch (value) {
                                    case 0:
                                        return "<i class='fa fa-times'></i>";
                                    case 1:
                                        return "<i class='fa fa-check'></i>";
                                    default:
                                        return value;
                                }
                            },
                            width: 100
                        },
                        {
                            id: "loglevel",
                            header: "Loglevel",
                            width: 100,
                            editor: "select",
                            options: [
                                {
                                    id: "none",
                                    value: "Disabled"
                                },
                                {
                                    id: "debug",
                                    value: "Debug"
                                },
                                {
                                    id: "info",
                                    value: "Info"
                                },
                                {
                                    id: "warning",
                                    value: "Warning"
                                },
                                {
                                    id: "error",
                                    value: "Error"
                                },
                                {
                                    id: "critical",
                                    value: "Critical"
                                }
                            ]
                        }
                    ]
                },
                {
                    view: "form",
                    id: "service_form",
                    borderless: true,
                    scroll: true,
                    elements: [
                    ]
                }
            ]
        }
    ]
};
