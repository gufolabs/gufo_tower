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
