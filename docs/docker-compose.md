# Docker-compose cheat sheet

```
$ docker-compose up -d                    # start containers in background
$ docker-compose stop                     # stop containers
$ docker-compose rm -v                    # remove stopped containers and volumes
$ docker-compose ps                       # see list of running containers
```

# Enter tower shell
```
$ docker-compose exec tower sh   
```

# Show current version
 
```
$ docker-compose images                   # tag and images id
```

# Update tower
```
$ docker-compose pull                     # get latest container version
$ docker-compose up -d                    # start containers in background
```

# View logs
```
$ docker-compose logs tower               # all logs
$ docker-compose logs -f tower            # see all and follow new logs
$ docker-compose logs -f --tail=10 tower  # show last 10 and follow. most useful one
```
