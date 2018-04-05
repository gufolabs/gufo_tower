# Migrate from mercurial to git

NOC for years was developed with mercurial. Now we are moved to git. Probably you are here cause of tower gives that url to you.

## Migration procedure

* Open `Additional services` tab in Tower.
* Click add button
* Fill the form like that
```
    Name: git_migrate
    Role name: git_migrate
    Enabled: tick
    leave description empty
    Link: git+https://code.getnoc.com/ansible-roles/ansible-role-git-migrate.git
```

* In services tabs tick git_migrate on nodes that are ready to be migrated.
* Save services.
* Open environment tabs and click deploy

## Migration notes

During migration process old noc directory will be partitionally droppped and replaced with new one from github. Old directory will be compressed to `noc_before_git_migrations.tbz`.

Your local modification will be placed to `/tmp/noc_diff.diff` that file will be used as patch after migration finished. Only not commited modifications will be transferred.

That role should be used only one time. So remove it after job done.

Be aware that if you have local modifications deploy process may fail with
```
      There are local modifications to /opt/noc directory. Local modification have to be placed to /opt/noc/custom directory.
      To continue update please do one of the following:
      * revert them `git checkout microservices`
      * stash them https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning
      for example
      ** `git stash`
      ** `git stash pop`
      * make merge request to https://code.getnoc.com/noc/noc with them
      * also you can change installation type to develop and resolve updates manually
```
You can drop local changes with
```
cd /opt/noc
git clean -f
git checkout -f microservices
```

### Deploy can fail during pip update


```
Traceback (most recent call last):
  File "./bin/pip", line 7, in <module>
    from pip import main
  File "/opt/noc/lib/python2.7/site-packages/pip/__init__.py", line 76, in <module>
    from pip.commands import commands, get_summaries, get_similar_commands
  File "/opt/noc/lib/python2.7/site-packages/pip/commands/__init__.py", line 6, in <module>
    from pip.commands.bundle import BundleCommand
  File "/opt/noc/lib/python2.7/site-packages/pip/commands/bundle.py", line 6, in <module>
    from pip.commands.install import InstallCommand
  File "/opt/noc/lib/python2.7/site-packages/pip/commands/install.py", line 5, in <module>
    from pip.req import InstallRequirement, RequirementSet, parse_requirements
  File "/opt/noc/lib/python2.7/site-packages/pip/req/__init__.py", line 3, in <module>
    from .req_install import InstallRequirement
  File "/opt/noc/lib/python2.7/site-packages/pip/req/req_install.py", line 42, in <module>
    from pip.utils.hashes import Hashes
  File "/opt/noc/lib/python2.7/site-packages/pip/utils/hashes.py", line 5, in <module>
    from pip.exceptions import HashMismatch, HashMissing, InstallationError
ImportError: cannot import name HashMissing

```

The only simple way to fix it is remove /opt/noc directory.
