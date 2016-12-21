Как постаивть нок для крупной инсталцяии > 10k устройст

h1. подготовка

* ставим docker
* ставим docker-compose
* export CONSUL_MASTER_TOKEN=$(uuidgen) CONSUL_ENCRYPTION_KEY=$(consul keygen)
* сохранить значения этих перменных в безопасных местах. в идеале вписать в сам файл c docker-compose
* docker-compouse up -d

На остальных нодах
* скачиваем consul в диретокрию /tmp
* запускаем sudo /tmp/consul agent -join=<TOWER_IP>  -data-dir /tmp -encrypt=<CONSUL_ENCRYPTION_KEY>
* на управляющей ноде
** проверяем что видим кластер
```
	./consul members
```
** выполняем команды аналогичные
```
	./consul exec -node="noc-debian" "adduser --home /home/ansible --shell /bin/sh ansible"
	./consul exec -node="noc-debian" "mkdir /home/ansible/.ssh/"
	./consul exec -node="noc-debian" "chown ansible:ansible -R /home/ansible/.ssh/"
	./consul exec -node="noc-debian" "apt update; apt-get install -y python2.7 sudo dbus; adduser ansible sudo"
	./consul exec -node="noc-debian" 'echo "ssh-rsa xxxxxxxx tower@localhost.localdomain" >> /home/ansible/.ssh/authorized_keys'
```

Начальное наполнение consul kv
абсолютный минимум
```
  {
    "Key": "noc/<ENV>/all",
    "CreateIndex": 245,
    "ModifyIndex": 511,
    "LockIndex": 0,
    "Flags": 0,
    "Value": "{\"ansible_ssh_private_key_file\": \"/opt/tower/var/tower/data/deploy_keys/id_rsa\",\"ansible_user\": \"ansible\"}",
    "Session": ""
  }
```

h1. Модель данных

Переменные уровня всего env.
noc/<ENV>/all -> json
noc/<ENV>/all/

        "alerta_token": "",
        "alerta_url": "",
        "ansible_python_interpreter": "/usr/bin/python2.7",
        "ansible_ssh_pipelining": true,
        "ansible_ssh_private_key_file": "/opt/tower/var/tower/data/deploy_keys/id_rsa",
        "ansible_user": "ansible",
        "noc_branch": "feature/microservices",
        "noc_changeset": "tip",
        "noc_custom_branch": "default",
        "noc_custom_changeset": "tip",
        "noc_custom_enabled": false,
        "noc_custom_repo": null,
        "noc_custom_revision": null,
        "noc_dc": "debian",
        "noc_env": "DEBIAN",
        "noc_env_type": "eval",
        "noc_group": "noc",
        "noc_installation_name": "Unconfigured installation",
        "noc_metrics_collector": "",
        "noc_repo": "http://192.168.1.46:8888/hg/VQ3W6R",
        "noc_revision": "feature/microservices",
        "noc_root": "/opt/noc",
        "noc_user": "noc",

Переменные для DC
noc/<ENV>/<DC> -> json
noc/<ENV>/<DC>/
        "proxy": "http://192.168.1.1:3128",
        "noc_metrics_collector": "http://local_collector:8086",

Переменные для всех сервисов
noc/<ENV>/<DC>/groups/all -> json
noc/<ENV>/<DC>/groups/all/
		пусто

Переменные для сервиса
noc/<ENV>/<DC>/groups/<SERVICE_NAME> -> json
noc/<ENV>/<DC>/groups/<SERVICE_NAME>/

        "noc_mongo_admin_password": "noc",
        "noc_mongo_admin_user": "root",
        "noc_mongo_db": "noc",
        "noc_mongo_password": "noc",
        "noc_mongo_replicaset": "noc",
        "noc_mongo_storageengine": "wiredTiger",
        "noc_mongo_user": "noc",
        "noc_pg_db": "noc",
        "noc_pg_password": "noc",
        "noc_pg_user": "noc",
        "noc_influxdb_db": "noc",
        "noc_influxdb_password": "noc",
        "noc_influxdb_user": "noc",
        "noc_web_host": "192.168.1.27",
        "noc_ssl_cert": "-----BEGIN CERTIFICATE-----",
        "noc_ssl_key": "-----BEGIN PRIVATE KEY-----",


noc/<ENV>/<DC>/groups/<NODE_NAME> -> json
noc/<ENV>/<DC>/groups/<NODE_NAME>/
        "ansible_host": "192.168.1.27",
        "has_svc_activator": true,
        "has_svc_bi": true,
        "has_svc_card": true,
        "has_svc_classifier": true,
        "has_svc_correlator": true,
        "has_svc_dev": true,
        "has_svc_discovery": true,
        "has_svc_escalator": true,
        "has_svc_grafana": true,
        "has_svc_grafanads": true,
        "has_svc_influxdb": true,
        "has_svc_login": true,
        "has_svc_mailsender": true,
        "has_svc_memcached": true,
        "has_svc_mongod": true,
        "has_svc_mongod_master": true,
        "has_svc_mrt": true,
        "has_svc_nginx": true,
        "has_svc_notebook": true,
        "has_svc_nsqadmin": true,
        "has_svc_nsqd": true,
        "has_svc_nsqlookupd": true,
        "has_svc_omap": true,
        "has_svc_pgbouncer": true,
        "has_svc_ping": true,
        "has_svc_pmwriter": true,
        "has_svc_postgres": true,
        "has_svc_postgres_master": true,
        "has_svc_sae": true,
        "has_svc_scheduler": true,
        "has_svc_syslogcollector": true,
        "has_svc_trapcollector": true,
        "has_svc_web": true,


принадлежность ноды окружению. хак.
noc/<ENV>/nodes/<NODE_NAME>
noc/<ENV>/<DC>/nodes/<NODE_NAME>
