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
    "datacenter": [],
    "environment": [
        "ansible_inventory"
    ],
    "login": [
        "change_password",
        "is_logged",
        "login",
        "logout"
    ],
    "node": [
        "prepare_node"
    ],
    "nodetype": [],
    "pool": [],
    "pull": [
        "get_job_status",
        "is_pulled",
        "start_job"
    ],
    "role": [],
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