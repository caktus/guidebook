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

## Adding Hosting Services Backups to a Project

This documentation is meant to clarify intent and process for developers who may want to add hosting 
services backup to their projects. [Site for the ansible role that does all of this](https://github.
com/caktus/ansible-role-k8s-hosting-services/).

NOTE: This documentation is primarily meant as reference. If your team doesn't want to set this up on your 
project yourself, you can ask the Sysadmin team to set up the backups on your project.

There are two components to setting up hosting services backups to a project.

1. The variable setup in your `host_vars/<environment_host>.yaml` and `k8s.yaml` files
2. Deploying the service into your projects cluster. (i.e. creating the service namespace and setting up the requested 
   cron jobs)

### Variable setup

For the majority of setups, you will need only a few variables.

#### Access Variables

These variables allow the Caktus Hosting services AWS Role to do work in your project.

Currently, this should be same on all projects.

```yaml
k8s_hosting_services_aws_access_key: <PROVIDED_BY_SYSADMIN>
k8s_hosting_services_aws_secret_access_key: <PROVIDED_BY_SYSADMIN>
```

#### Identification Variables

These variables identify key things about how you want your projects backups to be stored.

```yaml
# This could be any string that you want to use to help identify the backup folder
k8s_hosting_services_project_name: "<PROJECT_NAME>"
# This will be the folder that the backups are stored in.
k8s_hosting_services_namespace: "{{ k8s_hosting_services_project_name }}-hosting-services"
# The database that the service will be backing up. This will most likely already be set with
# this particular variable name.
k8s_hosting_services_database_url: "{{ env_database_url }}"
# This is the name of the S3 bucket. The `k8s_hosting_services_namespace` folder will be in here.
k8s_hosting_services_backup_base_bucket: investigator-portal-production-backups
# This is the name of the image that hosting services is using to do the backups.
k8s_hosting_services_image_tag: 0.4.0-postgres14
# The region your project is hosted in.
k8s_hosting_services_aws_region: "{{ aws_region }}"
```

#### Scheduling Variables

This is a single variable that tells the services the schedule of backups.

The below is just an example, you can configure this to suit your project.

```yaml
k8s_hosting_services_cron_schedules:
  - label: weekly
    schedule: "@weekly"
  - label: monthly
    schedule: "@monthly"
  - label: yearly
    schedule: "@yearly"
  - label: every2hours
    schedule: "0 */2 * * *"
```

#### Monitoring Variables

This is a variable that will be provided by the Sysadmin team.

```yaml
k8s_hosting_services_healthcheck_url: https://hc-ping.com/<UUID>
```

#### Location of the variables

This is dependant on the type of project that you have. If the project is simple you might have all of
these in one hosts file, or even in the `k8s.yaml` file.  A more complex project may split out the identification
level variables into separate host files.


### Deploying the Service

Once the variables are setup in your yaml files. Even if you commit, merge and deploy the code nothing 
will happen until you run the anisble playbook that uses the variables and wires everything up in the cluster.

The primary steps here are:

1. Add the role to your project.
2. Create a playbook to run the role.
3. Ensure your s3 buckets are configured.
4. Run the playbook.

The details for these steps are covered very well in the [ansible-role-k8s-hosting-services](https://github.
com/caktus/ansible-role-k8s-hosting-services) documentation.

NOTE: Once the jobs are created, they can only be removed via `kubectl` commands. If you change your backup 
schedule in the `k8s_hosting_services_cron_schedules`, and run the playbook again you will not remove the old
CRON job, and it will keep running until you remove it with `kubectl`.
