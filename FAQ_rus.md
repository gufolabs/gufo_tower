Типовые вопросы при установке с башни
=====================================

**В**: Зачем вообще нужна Tower ?

**О**: Конфигурация NOC разрослась настолько сильно, что сконфигурировать NOC на крупной инсталляции руками стало очень сложно.
Tower позволяет сделать service registry. Подробности можно почитать тут https://www.nginx.com/blog/service-discovery-in-a-microservices-architecture/

**В**: Что такое `Environment` ?

**О**: Это окружение. Грубо, со временем в компании появляется две и более установки системы, например одна для тестов, а другая рабочая.
Соответственно, можно задать в tower два окружения и управлять ими через нее.

**В**: В чем отиличие в типах `Environment` ?

**О**: На текущий момент отличие только одно. Инсталляция типа `Prod` заботиться о поддержании в чистоте каталога `/opt/noc`.
*Все файлы, которые не внесены в репозитарий, удаляются.* Если Это поведиене выглядит неразумным, используйте альтернативные варианты типов.

**В**: На какую систему лучше всего ставить NOC ?

**О**: Сейчас мы поддерживаем пять дистрибутитов.
RHEL 7+, Debian, Ubuntu, Centos и FreeBSD. Однако лучше всего тестируются RHEL 7 и Debian 8.
Установка на FreeBSD возможна, но сейчас для нее нет человека ее поддерживающего, поэтому может быть сломана.

**В**: Можно ли поставить Tower и NOC на один сервер?

**О**: Мы рекомендуем разделить командную ноду и саму систему.
С точки зрения последующей эксплуатации предполагается, что на Tower будет разворачиваться дополнительные инфраструктурные сервисы, анализатор логов, сбор метрик работы самой системы.
Однако поставить всё таки можно. Для этого при создании `node` надо задать вариант установки Linux/FreeBSD, позже в консоли выполнить следующие команды
 ```
 sqlite3 /opt/tower/var/tower/db/config.db
 update node_type set ansible_connection='local' where id=2;
 ```
соответственно `id=2` это FreeBSD. Однако, такая конфигурация совсем не тестируется и может поломаться.

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
* А так можно выполнить реконфигурацию системы. При этом рестарт системы будет плавным. Выключаться всё на время деплоя не будет. только последним шагом будет сделан плавный рестарт.
```
# su - tower
% cd /opt/tower/var/tower/playbooks/<NAME>/ansible/
% export ANSIBLE_SSH_PIPELINING=1 ANSIBLE_HOST_KEY_CHECKING=1 PYTHONUNBUFFERED=1 NOC_ENV=<NAME>
/opt/tower/bin/ansible-playbook -i /opt/tower/bin/tower-inv  site.yml -f 6  --tags config;
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

**В**: А где же deploy через `docker` ?

**О**: Пока нету. Будем думать об этом как только поймем, что делать с FreeBSD. https://wiki.freebsd.org/Docker

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
Дальше по обстоятельсвам.