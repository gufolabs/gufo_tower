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
    Link: `git+https://code.getnoc.com/ansible-roles/ansible-role-git-migrate.git`
```

* In services tabs tick git_migrate on nodes that are ready to be migrated. 
* Save services.
* Open environment tabs and click deploy

## Migration notes

During migration process old noc directory will be partitionally droppped and replaced with new one from github. Old directory will be compressed to `noc_before_git_migrations.tbz`.

Your local modification will be placed to `/tmp/noc_diff.diff` that file will be used as patch after migration finished. Only not commited modifications will be transferred. 
