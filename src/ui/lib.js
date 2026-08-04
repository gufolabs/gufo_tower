// ----------------------------------------------------------------------
// Tower.* functions
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

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
        check: function (v) {
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

export function threeStateCompare(value, filter) {
    if (filter == "thirdState") return true;
    return value == filter
}

webix.ui.datafilter.customFilterBool = {
    getInputNode: function (node) {
        return node.firstChild ? node.firstChild.firstChild : {
            indeterminate: true
        };
    },
    getValue: function (node) {
        var value = this.getInputNode(node).checked;
        var three = this.getInputNode(node).indeterminate;
        return three ? "thirdState" : value;
    },
    _stateSetter: function (e) {
        if (this.readOnly)
            this.checked = this.readOnly = false;
        else if (!this.checked)
            this.readOnly = this.indeterminate = true;
    },
    refresh: function (master, node, columnObj) {
        master.registerFilter(node, columnObj, this);
        node.querySelector("input").onclick = this._stateSetter;
        node.querySelector("input").indeterminate = true;
        node.querySelector("input").onchange = function () {
            master.filterByAll()
        }
    },
    render: function (master, column) {
        var html = "<input type='checkbox' id='cb1'>";
        return html;
    }
};