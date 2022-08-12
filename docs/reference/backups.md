# Backups


## Cutover Instructions


### Start one shell connected as the admin RDS user

```sh
inv pod.debian
apt update && apt install postgresql-client -y
export DATABASE_URL=...
psql $DATABASE_URL
```
**NOTE (requires invoke-kubsaea>=0.0.20)**: If you need a differenct version of debian so that you have the right postgressql-client you can specify it with `inv pod.debian --debian-flavor <bullseye:buster:stretch>`.

Run once replicas are scaled down:

```sql
DROP DATABASE mywebapp_production;
CREATE DATABASE mywebapp_production;

-- Connect to recreated DB and create extensions if needed
\c mywebapp_production;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS hstore;
```

### Restore instructions

```sh
# scale down (to release DB connections) and drop DB above
kubectl -n mywebapp-production scale deployment/app --replicas=0
# scale back up
kubectl -n mywebapp-production scale deployment/app --replicas=2
# restore DB
inv production pod.restore-db-from-dump --db-var="DATABASE_URL" --filename=mywebapp-archive.dump
```

### Post-restore tasks

1. Wagtail:
    1. Update `Site` object with correct domain.
2. Manually run migrations:

    ```shell
    kubectl -n mywebapp-production exec -it deploy/app -- python manage.py migrate
    ```
3. Manually create new superuser:

    ```shell
    kubectl -n mywebapp-production exec -it deploy/app -- python manage.py createsuperuser
    ```
