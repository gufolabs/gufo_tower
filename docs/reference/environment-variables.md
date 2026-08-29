# Environment Variables

Tower can be configured using the following environment variables.

| Variable                   | Default | Description                                                                                                                                                      |
| -------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TOWER_RUN_CHECKS`         | `False` | Run Ansible consistency checks during deployment. Disabling checks can save some time on well-maintained systems.                                                |
| `TOWER_SHOW_SECRETS`       | `False` | Run Ansible with secret data visible. When enabled, passwords, tokens, and other secrets may be displayed and saved in the deployment log. **Use with caution.** |
| `TOWER_RUN_TESTS`          | `False` | Run post-installation tests.                                                                                                                                     |
| `TOWER_STOP_NOC`           | `True`  | Stop NOC during deployment. Disabling this may reduce downtime on heavily loaded installations where deployment time is critical.                                |
| `TOWER_SERIAL_RESTART_NOC` | `False` | Restart NOC after installation using `./noc ctl serialrestart all`.                                                                                              |
| `TOWER_VERSION`            | —       | Internal variable used to verify that Tower generates the inventory correctly.                                                                                   |
| `TOWER_DB_PATH`            | —       | Internal variable specifying the path to the Tower `config.db` file.                                                                                             |
