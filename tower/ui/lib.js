Tower = {
    //
    // Validation rules
    //
    rules: {
        //
        // Check regular expression
        //
        regex: function(re) {
            return function(value) {
                return re.test(value);
            }
        }
    },
    msg: {
        started: function(message) {
            webix.message({
                type: "started",
                text: message,
                expire: 2000
            });
        },
        complete: function(message) {
            webix.message({
                type: "complete",
                text: message,
                expire: 2000
            });
        },
        failed: function(message) {
            webix.message({
                type: "failed",
                text: message,
                expire: 2000
            });
        },
        info: function(message) {
            webix.message({
                type: "info",
                text: message,
                expire: 2000
            });
        }
    }
};
