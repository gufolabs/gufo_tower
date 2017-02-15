Типовые вопросы при установке с башни
=====================================

**В**: Зачем вообще нужна Tower ?

**О**: Конфигурация NOC разрослась настолько сильно, что сконфигурировать NOC на крупной инсталляции руками стало очень сложно.
Tower позволяет сделать service registry. Подробности можно почитать тут https://www.nginx.com/blog/service-discovery-in-a-microservices-architecture/

**В**: Что такое `Environment` ?

**О**: Это окружение. Грубо, со временем в компании появляется две и более установки системы, например одна для тестов, а другая рабочая.
Соответственно, можно задать в tower два окружения и управлять ими через нее.

**В**: В чем отиличие в типах `Environment` ?

**О**: Есть несколько вещей которые дополнительно делаются для инсталляции типа Prod.
  * Инсталляция типа `Prod` заботится о поддержании в чистоте каталога `/opt/noc`. *Все файлы, которые не внесены в репозитарий, удаляются.* Если Это поведение выглядит неразумным, используйте альтернативные варианты типов.
  * Для этого типа инсталяции дополнительно открывается порт 9009 на прослушивание встроенным в `supervisord` http сервером. Для сбора информации о работе например в [nodervisor](https://github.com/TAKEALOT/nodervisor) или [cesi](https://github.com/gamegos/cesi).
  * Для этого типа инсталяции ставятся пакеты из файла `requirements/prod.txt`. Сейчас это утилита [alerta](http://docs.alerta.io/en/latest/)
  * Также копируется файл для совместной работы supervisord и alerta
Остальные варианты типов инсталяции не делают ничего дополнительного.

Обратите внимание, что при наличии правок в локальной директории при обновлении обновление NOC повиснет на этапе `Pull NOC`. В таком случае нужно зайти на ноду и решить вопрос с локлаьными правками:
  * Для начала имеет смысл остановить текущее обновление для этого находим в списке процессов `hg pull` и убиваем его. 
  * Выполняем либо 
    ** `hg revert -a ; hg --clean` - полная отчистка текущий директории от локальных правок. 
    ** `hg diff >/tmp/hg_diff.txt`  - бекапим изменения. в временный файл. позже после деплоя востанавливаем `hg import -f —no-commit /tmp/hg_diff.txt`
  * Бывает, что этого недостаточно и у вас есть правки которые попадают под категориюю `abort: untracked file in working directory differs from file in requested revision` поступаем с файлом по своему разумению.

**В**: На какую систему лучше всего ставить NOC ?

**О**: Сейчас мы поддерживаем пять дистрибутитов.
RHEL 7+, Debian, Ubuntu, Centos и FreeBSD. Однако лучше всего тестируются RHEL 7 и Debian 8.

**В**: Можно ли поставить Tower и NOC на один сервер?

**О**: Мы рекомендуем разделить командную ноду и саму систему.
С точки зрения последующей эксплуатации предполагается, что на Tower будет разворачиваться дополнительные инфраструктурные сервисы, анализатор логов, сбор метрик работы самой системы.
Однако поставить всё таки можно. Для этого при создании `node` надо задать вариант установки Linux/FreeBSD, позже в консоли выполнить следующие команды
 ```
 sqlite3 /opt/tower/var/tower/db/config.db
 update node_type set ansible_connection='local' where id=2;
 ```
соответственно `id=2` это FreeBSD.
Либо можно постаивть башню в виде docker контейнера.

**В**: Что такое `Node` ?

**О**: В терминологии системы нода - это сервер на котором будет крутится часть сервисов системы. Например DB или web-сервер.

**В**: Как должна быть настроена нода ?

**О**: На ноде должен быть:
 * создан пользователь ansible
 * пользователь ansible должен иметь возможность сделать `sudo -s` *без пароля*
 * на ноде должен быть установлен python2

**В**: Что делать с ошибкой `ERROR! SSH Error: data could not be sent to the remote host. Make sure this host can be reached over ssh", "unreachable"`?

**О**: Проверить так
 ```
 tower# su - tower
 tower% ssh ansible@host
 host% sudo -s
 host# python
 ```
Команды должны пройти легко и без ошибок.
Для инсталяции в докере убедиться, что выполнены (рекомендации)[https://groups.google.com/forum/#!topic/ansible-project/y8ohlv_dRi4] 

**В**: Как должен быть настроен сервер tower ?

**О**: В целом конфигурация описана в Readme.md. Однако в подробностях процесс выглядит так:
* Сам web сервис запускается из под пользователя tower. С консоли в простейшем случае или через systemd (см. `contrib/systemd`)
* Через web интерфейс принимается команда Deploy. Она выполняется из-под пользователя tower и условно делает следующие команды:
```
# su - tower
% cd /opt/tower/var/tower/playbooks/<NAME>/ansible/
% export ANSIBLE_SSH_PIPELINING=1 ANSIBLE_HOST_KEY_CHECKING=1 PYTHONUNBUFFERED=1 NOC_ENV=<NAME>
% /opt/tower/bin/ansible-playbook -i /opt/tower/bin/tower-inv  site.yml -f 50;
```
где `NAME` это имя заданное в названии `Environment`. После задания переменных и начальной конфигурации системы  можно вполне пользоваться консольными командами. А не нажимать кнопку в web-интерфейсе

**В**: В чем еще преимущества использования консоли вместо web ?

**О**: Там можно более точно управлять, что именно и как именно должно происходить. К примеру
* Пропустить все шаги playbook кроме обновления исходного кода.
```
# su - tower
% cd /opt/tower/var/tower/playbooks/<NAME>/ansible/
% export ANSIBLE_SSH_PIPELINING=1 ANSIBLE_HOST_KEY_CHECKING=1 PYTHONUNBUFFERED=1 NOC_ENV=<NAME>
/opt/tower/bin/ansible-playbook -i /opt/tower/bin/tower-inv  site.yml -f 6  --tags mercurial;
```
* А так можно выполнить реконфигурацию системы. При этом рестарт системы будет плавным. Выключаться всё на время деплоя не будет. Последним шагом будет сделан плавный рестарт.
```
# su - tower
% cd /opt/tower/var/tower/playbooks/<NAME>/ansible/
% export ANSIBLE_SSH_PIPELINING=1 ANSIBLE_HOST_KEY_CHECKING=1 PYTHONUNBUFFERED=1 NOC_ENV=<NAME>
/opt/tower/bin/ansible-playbook -i /opt/tower/bin/tower-inv  site.yml -f 6  --tags config,sort_restart;
```
В целом это может поломать deploy. Особенно когда происходят изменения в postgres схеме
Ну и конечно теги можно комбинировать примерно так `--tags config,mercurial` главное, не делать между ними пробелов
* Бывает что в результате каких то изменений коллекции ломаются. Обычно это выглядит вот так
```
TASK [migrate : Synchronize collections] ***************************************
fatal: [host]: FAILED! => {"changed": true, "cmd": ["./noc", "collection", "--sync"], "delta": "0:00:41.528846", "end": "2016-05-09 10:30:52.375631", "failed": true, "rc": 1, "start": "2016-05-09 10:30:10.846785", "stderr": "Error: Checksum mismatch for file 'XXX.json'", "stdout": "", "stdout_lines": [], "warnings": []}
```
в таких случаях процесс синхронизации коллекций можно временно пропустить, вот так
```
% NOC_ENV=<NAME> /opt/tower/bin/ansible-playbook -i /opt/tower/bin/tower-inv  site.yml -f 6  --skip-tags coll_sync
```

**В**: На чем написаны deploy скрипты?

**О**: На ansible. http://docs.ansible.com/ansible/intro.html

**В**: Где лежат deploy скрипты ?

**О**: В основном репозитарии [тут](https://bitbucket.org/nocproject/noc/src/e053b5692507e3fa67951873150fbca15d3cbcf5/ansible/?at=feature/microservices)

**В**: Я поставил по инструкции и все проверил, однако при инсталляции у меня ошибка. Где спросить помощи?

**О**: Можно тут https://telegram.me/nocproject

**В**: Где хранится конфиг services на башне?

**О**: В `/opt/tower/var/tower/db/config.db` в таблице `service` некоторые в `environment`.

**В**: Как диагностировать ошибку "No handlers could be found for logger \"noc.lib.nosql\""

**О**: Команды диагностики нужно выполнять на сервере с поставленным, пусть и не до конца, сервером noc
```
# cd /opt/noc
# ./noc shell
import logging
logging.basicConfig(level=logging.DEBUG)
from noc.sa.models.managedobject import ManagedObject
```
Дальше по обстоятельсвам. Чаще всего это означает, что слетеле авторизация в mongo.

**В**: Как поставить башню через `docker` ?

**О**: Довольно просто. Тут [реестр](https://code.getnoc.com/noc/tower/container_registry). Есть три типа контейнеров
* `master` - последняя доступная ревизия из `git`.
* `latest` - последняя стабильная версия.
* остальные. как правило, согласно выпущенным версиям.

Для утсновки можно использовать такой примерно `docker-compose.yml`
```
version: '2'
services:
  tower:
    image: registry.getnoc.com/noc/tower:master
    ports:
      - "8888:8888"
    volumes:
      - "/opt/tower/var:/opt/tower/var/"
      - "./root:/root"
    environment:
      http_proxy: http://192.168.0.1:3128
```
По желанию перед `tower` можно поставить `nginx` или добавить, что то еще. Каталог для `volume` произвольный.
В каталоге `/opt/tower/var/tower/data/deploy_keys` дожны лежать два файла - `id_rsa` и `id_rsa.pub`
Именно эти ключи будут использоваться для доступа к нодам.
При желании этот каталог тоже можно перемапить с помощью `docker` например так:
```
version: '2'
services:
  tower:
    image: registry.getnoc.com/noc/tower:master
    ports:
      - "8888:8888"
    volumes:
      - "/opt/tower/var:/opt/tower/var/"
      - "/etc/tower/keys:/opt/tower/var/tower/data/deploy_keys"
      - "./root:/root"
    environment:
      http_proxy: http://192.168.0.1:3128
```
Entrypoint скрипт если не обнаружит директорию с ключами создаст свои ключи.

**В**: Что означают опции развертывания?

**О**: После начальной инсталляции, как правило полный накат всего playbook не нужен, достаточно обновить исходники и рестартануть сервис.
Поэтому в башне есть несколько вариантов установки:
 * Install everything - первоначальная установка, проходит по всему playbook все ставит.
 * Update Sources - выполняет `hg pull -u` в директории noc и в директории custom
 * Update configs - конфигурирует все сервисы.
 * Install requirements - выполняет команды аналогичные ./bin/pip install -r requirements/noc.txt. Бывает полезно при впиливании каких то новых фич.
 * Do database migrations - проведет миграции базы. Для успешного выполнения требует полной остановки сервисов NOC.  Опция (Restart quick)

 Дальше идут подряд два варианта перезапуска NOC после применения `playbook`
 * Restart quick - делает рестарт нока средствами системы аналогично `/etc/init.d/noc restart`
 * Restart gentle - Делает рестарт средствами `supervisord`. Аналогично команде `./noc ctl serialrestart *`.
 Этот вариант перезапуска рекомендуется для крупных инсталляций, когда сервисов NOC больше, чем по одному, если выбраны оба варианта, побеждает этот.

Дальше идут подряд две опции отладки.
 * Be verbose  - аналогична ключу `-v` в `ansible-playbook`. Немного больше вывода.
 * Be extremelly verbose  - аналогична ключу `-vvvvv` в `ansible-playbook`. Режим отладки.

**В**: Есть ли возможность отказаться от использования Influxdb для внутреннего мониторинга ? 

**О**: Да, такая возможность есть. За возможность выбора мониторинга отвечают две переменные окружения:
 * PROMETHEUS_ENABLED - включает в telegraf слушатель для https://github.com/prometheus/prometheus/
 * INFLUXDB_ENABLED - включает отправку данных о телеметрии в  https://github.com/influxdata/influxdb. Выбран по умолчанию

 Возможно включение обоих сразу, однако какой то один должен быть включен всегда. Иначе telegraf просто не сможет стартануть. 
