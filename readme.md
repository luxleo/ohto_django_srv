# Server Config using docker compose

## 1. build image and download package for django

```
docker-compose up
```
### this stage will probably cause error So,

```
control + c: for escaping
```

## 2. second build for proper linking between container

```
docker-compose up
```
### after this command, all containers would be connected to each other

## 3. data push

### attach to django container to push song data

```
docker exec -i django-main sh
```
