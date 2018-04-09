# Environment variables used by tower

Several settings can be read from environment variables.

* `TOWER_RUN_CHECKS=` -- Run ansible checks. On well maintained system there is a way to save some time disabling consistency checks. Valid modes False(default), True.
* `TOWER_SHOW_SECRETS=`  -- Run ansible showing and saving all secret data. Passwords and tokens will be shown and saved to log in that mode. Valid modes False(default), True.
* `TOWER_RUN_TESTS=` -- Run after install tests.
* `TOWER_STOP_NOC=` --  Stop NOC during deploy. Should be helpfull on a heavy installations with lower time for downtime. Valid modes True(default), False.
* `TOWER_SERIAL_RESTART_NOC=` --  After install NOC will be restarted with `./noc ctl serialrestart all`. Valid modes False(default), True.
* `TOWER_VERSION=` -- Internal var. Used to check if tower generates inventory well.
* `TOWER_DB_PATH=` -- Internal var. Used to specify `config.db` path
