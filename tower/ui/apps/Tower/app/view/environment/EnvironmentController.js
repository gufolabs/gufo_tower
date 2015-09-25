Ext.define('Tower.view.environment.EnvironmentController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.environment-environment',
    requires: [
        "Ext.window.Toast",
        "Ext.window.MessageBox",
        "Ext.util.TaskManager"
    ],

    ITEM_GRID: 0,
    ITEM_FORM: 1,
    ITEM_INVENTORY: 2,
    ITEM_DEPLOY: 3,

    showGrid: function () {
        var me = this;
        me.getView().getLayout().setActiveItem(me.ITEM_GRID);
    },

    showForm: function () {
        var me = this;
        me.getView().getLayout().setActiveItem(me.ITEM_FORM);
    },

    onItemSelected: function (sender, record) {
        var me = this,
            form;
        form = me.lookupReference("form").getForm();
        form.reset();
        form.setValues(record.getData());
        me.getViewModel().set("record", record);
        me.showForm();
    },

    onRefresh: function () {
        var me = this;
        me.lookupReference("grid").getStore().reload();
    },

    onCreate: function () {
        var me = this;
        me.lookupReference("form").getForm().reset();
        me.getViewModel().set("recordId", null);
        me.showForm();
    },

    onCloseForm: function () {
        var me = this;
        me.showGrid();
    },

    onSave: function () {
        var me = this,
            form, data, record, store;
        form = me.lookupReference("form").getForm();
        data = form.getValues();
        store = me.lookupReference("grid").getStore();
        record = me.getViewModel().get("record");
        if (record) {
            // Edit
            record.set(data);
        } else {
            // Create
            record = store.add(data);
        }
        store.sync({
            success: function () {
                me.showGrid();
                Ext.toast({
                    html: "Data saved",
                    align: "t"
                });
            },
            failure: function () {
                Ext.Msg.alert("Failed to save");
            }
        });
    },

    onDelete: function () {
        var me = this,
            record, store;
        record = me.getViewModel().get("record");
        store = me.lookupReference("grid").getStore();
        store.remove(record);
        store.sync({
            success: function () {
                me.showGrid();
            },
            failure: function () {
                Ext.Msg.alert("Failed to delete record");
            }
        });
    },

    onInventory: function () {
        var me = this;
        API.Environment.ansible_inventory(
            me.getViewModel().get("selectedEnvironment").get("id"),
            function (result, status) {
                var html = "<pre>" + JSON.stringify(result, undefined, 2) + "</pre>";
                me.lookupReference("inventory").setHtml(html);
                me.getView().getLayout().setActiveItem(me.ITEM_INVENTORY);
            }
        )
    },

    onDeploy: function() {
        var me = this,
            envId;
        envId = me.getViewModel().get("selectedEnvironment").get("id");
        API.Pull.is_pulled(envId, function(result) {
            if(result) {
                me.deploy();
            } else {
                Ext.Msg.alert("Repo is not pulled. Pull repo first");
            }
        });
    },

    rxDeployProgress: /^(ok|changed|unreachable|failed|fatal): \[/mg,
    rxDeployTask: /^.+?\*{5}\s*$/mg,
    rxDeployLine: /^(ok|changed|unreachable|failed|fatal|skipping): \[.+?$/mg,

    deploy: function () {
        var me = this,
            envName, xhr, dp, vm,
            offset = 0;
        vm = me.getViewModel();
        envName = vm.get("selectedEnvironment").get("name");
        vm.set({
            deployStatus: false,
            nOk: 0,
            nChanged: 0,
            nUnreachable: 0,
            nFailed: 0
        });
        dp = me.lookupReference("deploy");
        dp.setHtml("");
        xhr = new XMLHttpRequest();
        xhr.open(
            "GET",
            Ext.String.format("/deploy/{0}/", envName),
            true
        );
        xhr.onprogress = function () {
            var ft = xhr.responseText,
                match, t, ct,
                dOk = 0, dChanged = 0, dUnreachable = 0, dFailed = 0;
            // Process only last chunk
            t = ft.substr(offset);
            offset = ft.length;
            // Get progress
            while (match = me.rxDeployProgress.exec(t)) {
                switch (match[1]) {
                    case "ok":
                        dOk += 1;
                        break;
                    case "changed":
                        dChanged += 1;
                        break;
                    case "unreachable":
                        dUnreachable += 1;
                        break;
                    case "failed":
                    case "fatal":
                        dFailed += 1;
                        break;
                }
            }
            // Update progress
            if (dOk + dChanged + dUnreachable + dFailed) {
                vm.set({
                    nOk: vm.get("nOk") + dOk,
                    nChanged: vm.get("nChanged") + dChanged,
                    nUnreachable: vm.get("nUnreachable") + dUnreachable,
                    nFailed: vm.get("nFailed") + dFailed
                });
            }
            // Update deploy log
            ct = t.replace(me.rxDeployTask, function (x) {
                return "<span class='ansible-task'>" + x + "</span>";
            });
            ct = ct.replace(me.rxDeployLine, function (x) {
                var c = x.split(":")[0];
                if (c === "fatal") {
                    c = "failed";
                }
                return "<span class='ansible-" + c + "'>" + x + "</span>";
            });
            dp.setHtml(
                (dp.html || "") + ct
            );
        };
        xhr.onload = function () {
            vm.set("deployStatus", true);
        };
        xhr.onerror = function () {
            vm.set("deployStatus", true);
        };
        me.getView().getLayout().setActiveItem(me.ITEM_DEPLOY);
        xhr.send();
    },

    onPull: function () {
        var me = this,
            pullButton, iconCls, deployButton, envId;
        envId = me.getViewModel().get("selectedEnvironment").get("id");
        pullButton = me.lookupReference("pullButton");
        deployButton = me.lookupReference("deployButton");
        pullButton.setDisabled(true);
        deployButton.setDisabled(true);
        iconCls = pullButton.iconCls;
        pullButton.setIconCls("x-fa fa-spinner fa-spin");
        API.Pull.start_job(envId, function (result) {
            var task, job,
                restore = function () {
                    deployButton.setDisabled(false);
                    pullButton.setDisabled(false);
                    pullButton.setIconCls(iconCls);
                    if (task) {
                        Ext.TaskManager.stop(task);
                    }
                },
                checkStatus = function () {
                    API.Pull.get_job_status(envId, job, function (result) {
                        if (!result.success) {
                            Ext.Msg.alert("Error", "Failed to pull");
                            restore();
                            return;
                        }
                        if (result.complete) {
                            if (!result.status) {
                                Ext.Msg.alert("Error", "Pull error");
                            } else {
                                Ext.toast({
                                    html: "Pull complete",
                                    align: "t"
                                });
                            }
                            restore();
                        }
                    });
                };
            if (!result.success) {
                Ext.Msg.alert("Error", "Failed to pull");
                restore();
                return;
            }
            job = result.job;
            task = Ext.TaskManager.start({
                interval: 1000,
                run: checkStatus
            });
        });
    }
});
