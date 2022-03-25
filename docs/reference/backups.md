# Backups


## Cutover Instructions


### Start one shell connected as the admin RDS user

```sh
inv pod.debian
apt update && apt install postgresql-client -y
export DATABASE_URL=...
psql $DATABASE_URL
```

Run once replicas are scaled down:

```sql
DROP DATABASE mywebapp_production;
CREATE DATABASE mywebapp_production;
GRANT CONNECT ON DATABASE mywebapp_production TO mywebapp_production;
GRANT ALL PRIVILEGES ON DATABASE mywebapp_production TO mywebapp_production;
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
