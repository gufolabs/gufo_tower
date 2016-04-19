Additional scripts
==================

That directory contains scripts used with systems based on systemd.

 * `noc-tower.service` should be placed to `/etc/systemd/system`
 * `noc-tower-backup.service` and `noc-tower-backup.timer` should be used together for backup. Backup directory is hardcoded with `/opt/tower_backup`. Also script will remove backup after 5 days. Fell free to change that values on your flavour.