var API = (function() {
    var r = {
        _base_url: "/api/",
        tid: 0
    };
    for(var api in SDL) {
        if(!SDL.hasOwnProperty(api)) {
            continue;
        }
        r[api] = {};
        for(var mi in SDL[api]) {
            var method = SDL[api][mi];
            r[api][method] = (function(r, api, method) {
                return function() {
                    var defer = webix.promise.defer();
                    webix.ajax().headers({
                        "Content-Type": "text/json"
                    }).post(
                        r._base_url + api + "/",
                        JSON.stringify({
                            id: r.tid++,
                            jsonrpc: "2.0",
                            method: method,
                            params: Array.prototype.slice.call(arguments)
                        })
                    ).then(function(resp) {
                        var data = resp.json();
                        if(!data.error) {
                            defer.resolve(data.result);
                        } else {
                            defer.reject(data.error);
                        }
                    }, function(err) {
                        defer.reject(err);
                    });
                    return defer;
                };
            })(r, api, method);
        }
    }
    return r;
})();


webix.proxy.rpc = {
    $proxy: true,

    load: function(view, callback, params) {
        API[this.source].get_items(params).then(
            function(data) {

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
