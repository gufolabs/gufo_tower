// ----------------------------------------------------------------------
// App State
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import { API } from "./rpc";
import { Tower } from "./lib";

class EventTrigger {
    #events = new EventTarget();

    fire() {
        this.#events.dispatchEvent(new Event("change"));
    }

    subscribe(callback) {
        this.#events.addEventListener("change", callback);
        return () => {
            this.#events.removeEventListener("change", callback);
        };
    }
}

class Store {
    #state;
    #events = new EventTarget();

    constructor(state) {
        this.#state = state;
    }

    get state() {
        return this.#state;
    }

    setState(updater) {
        const state =
            typeof updater === "function"
                ? updater(this.#state)
                : updater;
        if (state === this.#state) {
            return;
        }
        this.#state = state;
        this.#events.dispatchEvent(new Event("change"));
    }

    subscribe(callback) {
        this.#events.addEventListener("change", callback);
        return () => {
            this.#events.removeEventListener("change", callback);
        };
    }
}

class EnvStore extends Store {
    async with(env_id) {
        try {
            const env = await API.environment.get_item({ id: env_id });
            this.setState(env);
            return env;
        } catch (err) {
            Tower.msg.failed("Failed to get environment");
            throw err;
        }
    }
}

class PathStore extends Store {
    push(path = window.location.pathname) {
        if (path === "/login") {
            this.setState("/");
        } else {
            this.setState(path);
        }
    }

    pop() {
        const path = this.state;
        this.setState("/");
        return path;
    }
}

class SetStore extends Store {
    add(x) {
        this.setState((state) => {
            if (state.has(x)) {
                return state;
            }
            const next = new Set(state);
            next.add(x);
            return next;
        });
    }

    delete(x) {
        this.setState((state) => {
            if (!state.has(x)) {
                return state;
            }
            const next = new Set(state);
            next.delete(x);
            return next;
        });
    }
}

export const installation_name = new Store("Unconfigured installation");
export const current_env = new EnvStore(null);
export const return_path = new PathStore("/");
export const service_group = new Store("node");
export const deploy_options = new SetStore(new Set([1, 93, 94]));
export const on_deploy = new EventTrigger();