BEGIN TRANSACTION;
-- environment
-- CREATE TABLE IF NOT EXISTS "environment" (
--    "id" INTEGER NOT NULL PRIMARY KEY,
--    "name" VARCHAR(255) NOT NULL,
--    "description" TEXT NOT NULL,
--    "env_type" VARCHAR(255) NOT NULL,
--    "installation_name" VARCHAR(255) NOT NULL,
--    "web_host" VARCHAR(255) NOT NULL,
--    "is_default" INTEGER NOT NULL,
--    "config_order" VARCHAR(255) NOT NULL,
--    "install_method" VARCHAR(255) NOT NULL,
--    "playbook_link" VARCHAR(255) NOT NULL
-- );
INSERT INTO environment VALUES(1,'docs','The installation intended for the documentation purposes','test','Docs','simple.test.example.com',0,'yaml:///opt/noc/etc/tower.yml,yaml:///opt/noc/etc/settings.yml,env:///NOC','git','git+https://github.com/gufolabs/noc@stable');
-- settings
-- CREATE TABLE IF NOT EXISTS "settings" (
--     "key" VARCHAR(255) NOT NULL PRIMARY KEY,
--     "value" TEXT NOT NULL
-- );
-- INSERT INTO settings VALUES('cookie_secret','"63dpzLnGnP4H1PV6VnHVPPkfark0idyKUDZNPELfohqfmFwMNs2ye3bTXN+R/SXpGFCoV41YeA2gcBDxSOv8Tw=="');
INSERT INTO settings VALUES('installation_name','"Docs"');
INSERT INTO settings VALUES('url','"http://127.0.0.1:8888/"');
INSERT INTO settings VALUES('group_by','"service"');
-- datacenter
-- CREATE TABLE IF NOT EXISTS "datacenter" 
--     "id" INTEGER NOT NULL PRIMARY KEY, "name" VARCHAR(255) NOT NULL,
--     "description" TEXT NOT NULL,
--     "proxy" VARCHAR(255)
-- );
INSERT INTO datacenter VALUES(1,'dc1','default datacenter','');
-- pool
-- CREATE TABLE IF NOT EXISTS "pool" (
--     "id" INTEGER NOT NULL PRIMARY KEY,
--     "environment_id" INTEGER NOT NULL,
--     "name" VARCHAR(255) NOT NULL,
--     "description" TEXT NOT NULL,
--     FOREIGN KEY ("environment_id") REFERENCES "environment" ("id") ON DELETE RESTRICT
-- );
INSERT INTO pool VALUES(1,1,'default','Default pool for simple');
-- node
-- CREATE TABLE IF NOT EXISTS "node" (
--     "id" INTEGER NOT NULL PRIMARY KEY,
--     "environment_id" INTEGER NOT NULL,
--     "datacenter_id" INTEGER NOT NULL,
--     "name" VARCHAR(255) NOT NULL,
--     "description" TEXT NOT NULL,
--     "address" VARCHAR(255) NOT NULL,
--     "login_as" VARCHAR(255) NOT NULL,
--     "node_type_id" INTEGER REFERENCES "node_type" ("id") NOT NULL,
--     "is_enabled" INTEGER NOT NULL,
--     FOREIGN KEY ("environment_id") REFERENCES "environment" ("id") ON DELETE RESTRICT,
--     FOREIGN KEY ("datacenter_id") REFERENCES "datacenter" ("id") ON DELETE RESTRICT
-- );
INSERT INTO node VALUES(1,1,1,'n01','testing node','10.0.0.1','ansible',1,1);
-- role
-- CREATE TABLE IF NOT EXISTS "role" (
--     "id" INTEGER NOT NULL PRIMARY KEY,
--     "name" VARCHAR(255) NOT NULL,
--     "description" TEXT NOT NULL,
--     "link" VARCHAR(255) NOT NULL,
--     "environment_id" INTEGER NOT NULL,
--     "is_enabled" INTEGER NOT NULL,
--     "role_name" VARCHAR(255) NOT NULL,
--     FOREIGN KEY ("environment_id") REFERENCES "environment" ("id") ON DELETE RESTRICT
-- );
INSERT INTO role VALUES(1,'Custom','Custom NOC role','git+https://code.getnoc.com/ansible-roles/ansible-role-custom.git',1,0,'custom');
INSERT INTO role VALUES(2,'Sentry','Provides configuration settings for Sentry','git+https://code.getnoc.com/ansible-roles/ansible-role-sentry.git',1,0,'sentry');
INSERT INTO role VALUES(3,'Pgbouncer','Helps to handle thousand of devices. From 1k devices','git+https://code.getnoc.com/ansible-roles/ansible-role-pgbouncer.git',1,1,'pgbouncer');
INSERT INTO role VALUES(4,'Memcached','Caching level. Helps to handle lots of devices. From 20k devices.','git+https://code.getnoc.com/ansible-roles/ansible-role-memcached.git',1,0,'memcached');
INSERT INTO role VALUES(5,'Alerta notifications','Notifies about deploy to deploy system','git+https://code.getnoc.com/ansible-roles/ansible-role-alerta-notifications.git',1,0,'deploy_notification');
INSERT INTO role VALUES(6,'Telegraf','Helps to monitor node''s health','git+https://code.getnoc.com/ansible-roles/ansible-role-telegraf.git',1,0,'telegraf');
INSERT INTO role VALUES(7,'Nsqadmin','Web interface for NSQd','git+https://code.getnoc.com/ansible-roles/ansible-role-nsqadmin.git',1,0,'nsqadmin');
-- service
-- CREATE TABLE IF NOT EXISTS "service" (
--     "id" INTEGER NOT NULL PRIMARY KEY,
--     "environment_id" INTEGER NOT NULL,
--     "service" VARCHAR(255) NOT NULL,
--     "pool_id" INTEGER, "node_id" INTEGER NOT NULL,
--     "config" TEXT NOT NULL, "present" INTEGER NOT NULL
--     FOREIGN KEY ("environment_id") REFERENCES "environment" ("id") ON DELETE RESTRICT,
--     FOREIGN KEY ("pool_id") REFERENCES "pool" ("id"),
--     FOREIGN KEY ("node_id") REFERENCES "node" ("id")
-- );
INSERT INTO service VALUES(1,1,'kafkasender',NULL,1,'{"backup_power": 1, "bootstrap_servers": "", "loglevel": "info", "password": "", "power": 1, "sasl_mechanism": "PLAIN", "security_protocol": "PLAINTEXT", "username": ""}',0);
INSERT INTO service VALUES(2,1,'discovery',1,1,'{"backup_power": 1, "loglevel": "info", "max_threads": 20, "power": 2}',0);
INSERT INTO service VALUES(3,1,'mx',NULL,1,'{"loglevel": "info", "power": 1}',0);
INSERT INTO service VALUES(4,1,'mib',NULL,1,'{"loglevel": "info", "power": 1}',0);
INSERT INTO service VALUES(5,1,'grafanads',NULL,1,'{"db_threads": 10, "loglevel": "info", "power": 2}',0);
INSERT INTO service VALUES(6,1,'trapcollector',1,1,'{"listen": "0.0.0.0:162", "loglevel": "info", "permit_firewall": true, "power": 1}',0);
INSERT INTO service VALUES(7,1,'metrics',NULL,1,'{"backup_power": 1, "loglevel": "info", "power": 2}',0);
INSERT INTO service VALUES(8,1,'scheduler',NULL,1,'{"loglevel": "info", "max_threads": 10, "power": 1}',0);
INSERT INTO service VALUES(9,1,'noc',NULL,1,'{"consul_token": "noc", "group": "noc", "py3_ver": "3.10", "repo": "https://github.com/nocproject/noc.git", "root": "/opt/noc", "user": "noc", "version": "stable"}',0);
INSERT INTO service VALUES(10,1,'login',NULL,1,'{"language": "en", "loglevel": "info", "methods": "local", "pam_service": "noc", "power": 2, "radius_secret": null, "radius_server": null, "session_ttl": "7d"}',0);
INSERT INTO service VALUES(11,1,'kafka',NULL,1,'{"cluster_id": "", "insecure_certs": false, "memory_limit": 1}',0);
INSERT INTO service VALUES(12,1,'postgres',NULL,1,'{"max_clients": 300, "noc_db": "noc", "noc_password": "noc", "noc_user": "noc", "power": "master", "replicator_password": "noc", "superuser_password": "noc", "version": "14"}',0);
INSERT INTO service VALUES(13,1,'nginx',NULL,1,'{"cert": null, "cert_key": null, "external_cert_management": "False", "http_redirect": "True", "json_logging": "False", "permit_firewall": true, "self_signed_cerificate": "True"}',0);
INSERT INTO service VALUES(14,1,'mongod',NULL,1,'{"db": "noc", "logging_destination": "syslog", "password": "noc", "power": "server", "rs": "noc", "user": "noc", "version": "4.4"}',0);
INSERT INTO service VALUES(15,1,'nbi',NULL,1,'{"loglevel": "info", "power": 1, "whitelist_access": ""}',0);
INSERT INTO service VALUES(16,1,'mrt',NULL,1,'{"loglevel": "info", "max_concurrency": 50, "power": 2}',0);
INSERT INTO service VALUES(17,1,'goss',NULL,1,'{"validate_fw": true, "version": "0.3.22"}',0);
INSERT INTO service VALUES(18,1,'classifier',1,1,'{"backup_power": 1, "default_interface_profile": "default", "loglevel": "info", "lookup_solution": "noc.services.classifier.rulelookup.RuleLookup", "power": 2}',0);
INSERT INTO service VALUES(19,1,'mailsender',NULL,1,'{"from_address": "noc@example.com", "helo_hostname": "noc", "loglevel": "info", "power": 1, "smtp_password": null, "smtp_port": 25, "smtp_server": null, "smtp_user": null, "use_tls": "False"}',0);
INSERT INTO service VALUES(20,1,'syslogcollector',1,1,'{"listen": "0.0.0.0:514", "loglevel": "info", "permit_firewall": true, "power": 1}',0);
INSERT INTO service VALUES(21,1,'sae',NULL,1,'{"db_threads": 4, "loglevel": "info", "power": 2}',0);
INSERT INTO service VALUES(22,1,'selfmon',NULL,1,'{"enable_fm": false, "enable_inventory": false, "enable_liftbridge": false, "enable_managedobject": true, "enable_task": false, "loglevel": "info", "power": 1}',0);
INSERT INTO service VALUES(23,1,'consul-template',NULL,1,'{"own_install": false, "use_dedup": "False"}',0);
INSERT INTO service VALUES(24,1,'ui',NULL,1,'{"loglevel": "info", "power": 2}',0);
INSERT INTO service VALUES(25,1,'card',NULL,1,'{"language": "en", "loglevel": "info", "power": 2}',0);
INSERT INTO service VALUES(26,1,'tgsender',NULL,1,'{"loglevel": "info", "power": 1, "proxy_address": null, "token": null, "use_proxy": false}',0);
INSERT INTO service VALUES(27,1,'worker',NULL,1,'{"backup_power": 1, "loglevel": "info", "power": 2}',0);
INSERT INTO service VALUES(28,1,'grafana',NULL,1,'{"own_install": false, "pg_password": "grafana"}',0);
INSERT INTO service VALUES(29,1,'liftbridge',NULL,1,'{"liftbridge_insecure": false, "loglevel": "info"}',0);
INSERT INTO service VALUES(30,1,'activator',1,1,'{"loglevel": "info", "power": 2, "script_threads": 20, "tos": 0}',0);
INSERT INTO service VALUES(31,1,'bi',NULL,1,'{"language": "en", "loglevel": "info", "power": 2, "query_threads": 10}',0);
INSERT INTO service VALUES(32,1,'nats',NULL,1,'{"cluster_password": "noc", "cluster_user": "noc", "loglevel": "info", "nats_insecure": false}',0);
INSERT INTO service VALUES(33,1,'escalator',NULL,1,'{"loglevel": "info", "max_threads": 10, "power": 1}',0);
INSERT INTO service VALUES(34,1,'ping',1,1,'{"backup_power": 1, "loglevel": "info", "power": 4, "restore_threshold": 0, "throttle_threshold": 0, "tos": 0}',0);
INSERT INTO service VALUES(35,1,'correlator',1,1,'{"backup_power": 1, "loglevel": "info", "max_threads": 10, "power": 1}',0);
INSERT INTO service VALUES(36,1,'bh',NULL,1,'{"loglevel": "info", "power": 2}',0);
INSERT INTO service VALUES(37,1,'chwriter',NULL,1,'{"batch_delay_ms": 1000, "batch_size": 50000, "channel_expire_interval": 300, "loglevel": "info", "power": 1, "records_buffer": 1000000}',0);
INSERT INTO service VALUES(38,1,'clickhouse',NULL,1,'{"db": "noc", "expose_metrics": true, "max_ast_elements": 10000, "password": "noc", "query_size": 262144, "ro_grafana_password": "noc", "ro_password": "noc", "timezone": "Europe/Moscow", "user": "noc"}',0);
INSERT INTO service VALUES(39,1,'consul',NULL,1,'{"address": "node_ip", "master_token": null, "own_install": false, "power": "bootstrap", "replication_token": null, "setup_resolv": false}',0);
INSERT INTO service VALUES(40,1,'datastream',NULL,1,'{"enable_address": false, "enable_address_wait": false, "enable_administrativedomain": false, "enable_administrativedomain_wait": false, "enable_alarm": false, "enable_alarm_wait": false, "enable_cfgping": true, "enable_cfgping_wait": true, "enable_cfgsyslog": true, "enable_cfgsyslog_wait": true, "enable_cfgtrap": true, "enable_cfgtrap_wait": true, "enable_dnszone": false, "enable_dnszone_wait": false, "enable_managedobject": false, "enable_managedobject_wait": false, "enable_prefix": false, "enable_prefix_wait": false, "enable_resourcegroup": false, "enable_resourcegroup_wait": false, "enable_vrf": false, "enable_vrf_wait": false, "loglevel": "info", "mode": "wait", "power": 1, "whitelist_access": ""}',0);
INSERT INTO service VALUES(41,1,'web',NULL,1,'{"language": "en", "loglevel": "info", "max_threads": 10, "power": 2, "theme": "gray"}',0);
INSERT INTO service VALUES(42,1,'pgbouncer',NULL,1,'{"max_clients": 2000, "max_db_connections": 10, "timezone": "Europe/Moscow"}',0);
COMMIT;
