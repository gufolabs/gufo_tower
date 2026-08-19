// ----------------------------------------------------------------------
// App State
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

export class AppState {
    current_env = null;
    return_path = "/";

    set_environment = (env) => {
        this.current_env = env;
    }

    clear_environment = () => {
        this.current_env = null;
    }

    get_environment = () => {
        return this.current_env;
    }

    push_return_path = (path) => {
        path = path ?? window.location.pathname;
        if (path === "/login") {
            this.return_path = "/";
        } else {
            this.return_path = path;
        }
    }

    pop_return_path = () => {
        const path = this.return_path;
        this.return_path = "/";
        return path;
    }
};

export const state = new AppState();