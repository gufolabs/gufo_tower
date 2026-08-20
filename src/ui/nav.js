// ----------------------------------------------------------------------
// Navigation items
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

export const short_navigation = [
    {
        id: "home",
        value: "Home",
        icon: "home",
        path: "/"
    },
    {
        id: "environment",
        value: "Environments",
        icon: "cloud",
        path: "/environment"
    },
    {
        id: "datacenter",
        value: "Datacenters",
        icon: "building",
        path: "/datacenter"
    },
    {
        id: "settings",
        value: "Settings",
        icon: "cog",
        path: "/settings"
    }
];

export const full_navigation = [
    {
        id: "home",
        value: "Home",
        icon: "home",
        path: "/"
    },
    {
        id: "environment",
        value: "Environments",
        icon: "cloud",
        path: "/environment"
    },
    {
        id: "datacenter",
        value: "Datacenters",
        icon: "building",
        path: "/datacenter"
    },
    {
        id: "pool",
        value: "Pools",
        icon: "files-o",
        path: "/environment/:id/pool"
    },
    {
        id: "node",
        value: "Nodes",
        icon: "server",
        path: "/environment/:id/node"
    },
    {
        id: "service",
        value: "Services",
        icon: "cubes",
        path: "/environment/:id/service"
    },
    {
        id: "role",
        value: "Additional services",
        icon: "archive",
        path: "/environment/:id/role"
    },
    {
        id: "settings",
        value: "Settings",
        icon: "cog",
        path: "/settings"
    }
];