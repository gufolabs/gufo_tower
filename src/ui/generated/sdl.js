// ------------------------------------------------------------------------
// RPC contract
// WARNING!
// Auto-generated file! Do not modify manually.
// To update use:
//    python scripts/build-generated.py
// ------------------------------------------------------------------------
// Copyright 2015-2026 Gufo Labs
// ------------------------------------------------------------------------
export const SDL = {
    "datacenter": [
        "create_item",
        "delete_item",
        "get_items",
        "lookup_items",
        "update_item"
    ],
    "environment": [
        "ansible_inventory",
        "create_item",
        "delete_item",
        "get_items",
        "lookup_items",
        "update_item"
    ],
    "home": [
        "get_data"
    ],
    "login": [
        "change_password",
        "is_logged",
        "login",
        "logout"
    ],
    "node": [
        "create_item",
        "delete_item",
        "get_items",
        "lookup_items",
        "prepare_node",
        "update_item"
    ],
    "nodetype": [
        "create_item",
        "delete_item",
        "get_items",
        "lookup_items",
        "update_item"
    ],
    "pool": [
        "create_item",
        "delete_item",
        "get_items",
        "lookup_items",
        "update_item"
    ],
    "pull": [
        "get_job_status",
        "is_pulled",
        "start_job"
    ],
    "role": [
        "create_item",
        "delete_item",
        "get_items",
        "lookup_items",
        "update_item"
    ],
    "service": [
        "get_forms",
        "get_service_list",
        "save_config"
    ],
    "settings": [
        "get_settings",
        "save_settings"
    ]
};