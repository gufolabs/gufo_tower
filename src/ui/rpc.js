// ----------------------------------------------------------------------
// API and RPC wrapper
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------
import { SDL } from "./generated/sdl.js";

export const API = (function () {
    const r = {
        _base_url: "/api/",
        tid: 0
    };
    for (const api in SDL) {
        if (!Object.hasOwn(SDL, api)) {
            continue;
        }
        r[api] = {};
        for (const mi in SDL[api]) {
            const method = SDL[api][mi];
            r[api][method] = (function (rr, rpc_api, http_method) {
                return async function () {
                    const resp = await fetch(
                        rr._base_url + rpc_api + "/",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type": "text/json"
                            },
                            body: JSON.stringify({
                                id: rr.tid++,
                                jsonrpc: "2.0",
                                method: http_method,
                                params: Array.prototype.slice.call(arguments)
                            })
                        }
                    );
                    if (!resp.ok) {
                        throw new Error(`HTTP ${resp.status}`);
                    }
                    const data = await resp.json();
                    if (data.error) {
                        throw data.error;
                    }
                    return data.result;
                };
            })(r, api, method);
        }
    }
    return r;
})();


webix.proxy.rpc = {
    $proxy: true,

    load: function (view, callback, params) {
        const r = { dynamic: true };
        let state = {},
            source = this.source,
            i, j, p, v, method;
        if (view.getState) {
            state = view.getState();
        }
        if (state.sort) {
            // Todo: Convert to list
            r.sort = state.sort;
        }
        // Strip query from url
        if ((i = source.indexOf("?")) !== -1) {
            p = source.substring(i + 1).split("&");
            // Process parameters
            for (j in p) {
                v = p[j].split("=");
                if ((v[0] === "start") || (v[0] === "count")) {
                    r[v[0]] = parseInt(v[1]);
                }
            }
            source = source.substring(0, i);
        }
        if (source.substring(source.length - 7) === ":lookup") {
            // Combo lookup
            source = source.substring(0, source.length - 7);
            method = "lookup_items";
        } else {
            method = "get_items";
        }
        API[source][method](r).then(
            function (data) {
                webix.ajax.$callback(
                    view,
                    callback,
                    JSON.stringify(data),  // Need to pass JSON object
                    data
                );
            }
        );
    }
};
