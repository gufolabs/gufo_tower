// ----------------------------------------------------------------------
// Application route
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

export class Route {
    constructor(pattern, handler, menu = null) {
        this.pattern = pattern;
        this.handler = handler;
        this.menu = menu;
    }

    match(path) {
        const match = path.match(this.pattern);
        if (!match) {
            return null;
        }
        return match.slice(1);
    }

    async show(path) {
        const params = this.match(path);
        if (params === null) {
            return false;
        }

        await this.handler(...params);
        if (this.menu !== null) {
            $$("sidebar").select(this.menu, false);
        }
        return true;
    }
}

export class Router {
    constructor(routes = []) {
        this.routes = routes;
        this.last_path = null;
    }

    async show(path) {
        path = path ?? window.location.pathname;
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

    push = (...routes) => {
        this.routes.push(...routes);
    };
}

export const router = new Router();