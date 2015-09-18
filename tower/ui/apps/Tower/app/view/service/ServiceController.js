Ext.define('Tower.view.service.ServiceController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.service-service',

    onActiveApp: function() {
        var me = this,
            vm = me.getViewModel(),
            env = vm.get("selectedEnvironment"),
            grid = me.lookupReference("grid"),
            poolsCombo = me.lookupReference("poolsCombo"),
            servicesCombo = me.lookupReference("servicesCombo");
        // Get current settings
        API.Service.get_data(env.get("id"), function(result) {
            // Fill Pools combo
            poolsCombo.getStore().loadData(result.pools);
            // Fill Services combo
            servicesCombo.getStore().loadData(result.services);
            //
            me.svcCfg = {
                nodes: result.nodes,
                svccfg: {}  // pool -> service -> node -> {n_instances, loglevel}
            };
            Ext.each(result.pools, function(p) {
                me.svcCfg.svccfg[p.id] = {};
            });
            Ext.each(result.svccfg, function(p) {
                var pc = me.svcCfg.svccfg[p.pool];
                if(!pc[p.service]) {
                    pc[p.service] = {};
                }
                pc[p.service][p.node] = {
                    n_instances: p.n_instances,
                    loglevel: p.loglevel
                };
            });
        });
    },

    onSelect: function(combo, record) {
        var me = this,
            pv, sv, sc, ss, changePool, data = [];
        pv = me.lookupReference("poolsCombo").getValue();
        sv = me.lookupReference("servicesCombo").getValue();
        changePool = combo.reference === "poolsCombo";
        if(changePool) {
            ss = me.lookupReference("servicesCombo").getStore();
            ss.clearFilter();
            ss.filterBy(function(r) {
                var isPooled = r.get("level") === "pool";
                return (
                    (pv === 0 && !isPooled) ||
                    (pv > 0 && isPooled)
                );
            });
        }
        if(pv === null || sv === null) {
            return;
        }
        // Fill grid
        sc = me.svcCfg.svccfg[pv][sv];
        Ext.each(me.svcCfg.nodes, function(n) {
            var ni = 0, ll = "info";
            if(sc && sc[n.id]) {
                ni = sc[n.id].n_instances;
                ll = sc[n.id].loglevel;
            }
            data.push({
                id: n.id,
                name: n.name,
                datacenter: n.datacenter,
                n_instances: ni,
                loglevel: ll
            });
        });
        me.lookupReference("grid").getStore().loadData(data);
    },

    onServiceEdit: function(editor, ctx) {
        var me = this,
            pv, sv;
        pv = me.lookupReference("poolsCombo").getValue();
        sv = me.lookupReference("servicesCombo").getValue();
        if(!me.svcCfg.svccfg[pv][sv]) {
            me.svcCfg.svccfg[pv][sv] = {};
        }
        me.svcCfg.svccfg[pv][sv][ctx.record.get("id")] = {
            n_instances: ctx.record.get("n_instances"),
            loglevel: ctx.record.get("loglevel")
        };
        me.lookupReference("saveButton").setDisabled(false);
    },

    onSave: function() {
        var me = this,
            envId, p, s, n, c,
            data = [],
            sc = me.svcCfg.svccfg;
        envId = me.getViewModel().get("selectedEnvironment").get("id");
        // Flatten config to list
        for(p in sc) {
            for(s in sc[p]) {
                for(n in sc[p][s]) {
                    c = sc[p][s][n];
                    data.push({
                        pool: p,
                        service: s,
                        node: n,
                        n_instances: c.n_instances,
                        loglevel: c.loglevel
                    });
                }
            }
        }
        //
        API.Service.save_services(envId, data, function() {
            me.lookupReference("saveButton").setDisabled(true);
        });
    }
});
