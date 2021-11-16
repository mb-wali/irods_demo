## build irods image

```
./build.sh
```

## run irods ICAT server
```
docker-compose.yml up -d
```


## create users

```
    ${DOCKER_COMPOSE} exec --user irods irods-provider bash -c "iadmin mkuser jim rodsuser"
    ${DOCKER_COMPOSE} exec --user irods irods-provider bash -c "iadmin moduser jim password ${JIM_PASSWORD}"
    ${DOCKER_COMPOSE} exec --user irods irods-provider bash -c "iadmin mkuser jon rodsuser"
    ${DOCKER_COMPOSE} exec --user irods irods-provider bash -c "iadmin moduser jon password ${JON_PASSWORD}"
```

## errors
* Consumer server is not working properly
