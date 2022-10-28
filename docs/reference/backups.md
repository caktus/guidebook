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

### Restore instructions (kubectl)

```sh
# scale down (to release DB connections) and drop DB above
kubectl -n mywebapp-production scale deployment/app --replicas=0
# scale back up
kubectl -n mywebapp-production scale deployment/app --replicas=2
# restore DB
inv production pod.restore-db-from-dump --db-var="DATABASE_URL" --filename=mywebapp-archive.dump
```

**NOTE:**

If your stack has celery installed then you will need to scale those down as well to free resources:

### Restore instructions (invoke-kubesae)

As of version `0.0.21` invoke-kubesae, has a utility command `utils.scale-app` to help with this.

#### Usage Examples

```shell
 > inv staging utils.scale-app --down  # Scales the containers to 0.
 > inv staging utils.scale-app --down --celery  # Scales the containers, celery-worker, and celery-beat to 0.
 > inv staging utils.scale-app  # Scales the containers to 2.
 > inv staging utils.scale-app --celery  # Scales the containers to 2, and celery-worker/celery-beat to 1.
 > inv staging utils.scale-app --container-count 4  # Scales the containers to 4.
 > inv staging utils.scale-app --container-count 4 --celery  # Scales the containers to 4, and celery-worker/celery-beat to 1.
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
