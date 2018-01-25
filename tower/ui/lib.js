Tower = {
    //
    // Validation rules
    //
    rules: {
        //
        // Check regular expression
        //
        regex: function (re) {
            return function (value) {
                return re.test(value);
            }
        }
    },
    msg: {
        started: function (message) {
            webix.message({
                type: "started",
                text: message,
                expire: 2000
            });
        },
        complete: function (message) {
            webix.message({
                type: "complete",
                text: message,
                expire: 2000
            });
        },
        failed: function (message) {
            webix.message({
                type: "failed",
                text: message,
                expire: 2000
            });
        },
        info: function (message) {
            webix.message({
                type: "info",
                text: message,
                expire: 2000
            });
        }
    },
    format: {
        lookup: function (v) {
            if (v.id === undefined) {
                return v;
            } else {
                return v.value;
            }
        },
        check: function(v) {
            if (v) {
                return "<i class='fa fa-check'></i>";
            }
            return "<i class='fa fa-times'></i>";
        }
    },
    notification: function (v) {
        if (!("Notification" in window)) {
            return; // Not supported
        }
        if (Notification.permission === "granted") {
            new Notification(v);
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission(function (permission) {
                if (permission === "granted") {
                    new Notification(v);
                }
            });
        }
    }
};
