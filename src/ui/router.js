// ----------------------------------------------------------------------
// Application router
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

export class Router {
    constructor(routes = []) {
        this.routes = routes;
        this.last_path = null;
    }

    async show(path) {
        if (this.last_path === path) {
            return true;
        }
        for (const route of this.routes) {
            if (await route.show(path)) {
                this.last_path = path;
                return true;
            }
        }
        return false;
    }

    init = () => {
        navigation.addEventListener("navigate", (event) => {
            if (!event.canIntercept) {
                return;
            }
            event.intercept({
                handler: async () => {
                    const url = new URL(event.destination.url);
                    await this.show(url.pathname);
                },
            });
        });
    }
}