Ext.define("Tower.model.Environment", {
    extend: "Ext.data.Model",
    fields: [
        {name: "id", type: "string"},
        {name: "name", type: "string"},
        {name: "description", type: "string"},
        {name: "env_type", type: "string"},
        {name: "sys_user", type: "string"},
        {name: "sys_group", type: "string"},
        {name: "sys_prefix", type: "string"},
        {name: "repo", type: "string"},
        {name: "branch", type: "string"},
        {name: "changeset", type: "string"},
        {name: "web_host", type: "string"},
        {name: "pg_db", type: "string"},
        {name: "pg_user", type: "string"},
        {name: "pg_password", type: "string"},
        {name: "mongo_db", type: "string"},
        {name: "mongo_user", type: "string"},
        {name: "mongo_password", type: "string"},
        {name: "mongo_rs", type: "string"},
        {name: "mongo_engine", type: "string"}
    ]
});
