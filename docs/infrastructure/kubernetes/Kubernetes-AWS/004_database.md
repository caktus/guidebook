# Database configuration

## PostgreSQL RDS

Choose the latest version of PostgreSQL RDS [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts.General.DBVersions). You can also run:

```shell
aws rds describe-db-engine-versions --default-only --engine postgres
```

Pick a version of postgres you want for the project.

Newer versions of postgres may not be configured in [Caktus AWS Web Stacks](https://github.com/caktus/aws-web-stacks).

Check [here to see](https://github.com/caktus/aws-web-stacks/blob/31859d5c935653be453f97220f2e53155e23f429/stack/database.py#L169) if 
the version you are targeting is listed. If it is not, open a PR to have it added.

You will add your selected version of Postgres to the `DatabaseParameterGroupFamily` variable found in the [WebStacks section](005_cloudformation.md#configure-the-ansible-variables) of
the `deploy/group_vars/all.yaml` file.


## 🗄️ Create PostgreSQL databases

#### Temporary pod:

Launch a temporary Debian pod within the cluster

```sh
inv pod.debian
```

#### Install postgres client

The temporary pods don't have much in them, so you will need to install `postgresql-client` and connect to the RDS PostgreSQL cluster as the admin user.
The Admin 

```sh
apt update && apt install postgresql-client -y
export DATABASE_URL=...
psql $DATABASE_URL
```

3. Create the environment's role::

```sql
CREATE ROLE <<PROJECT_NAME>>_<<ENVIRONMENT>> WITH LOGIN NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION PASSWORD '<password1>';
```

4. Create environment-specific databases, e.g.::

```sql
CREATE DATABASE <<PROJECT_NAME>>_<<ENVIRONMENT>>;
GRANT CONNECT ON DATABASE <<PROJECT_NAME>>_<<ENVIRONMENT>> TO <<PROJECT_NAME>>_<<ENVIRONMENT>>;
GRANT ALL PRIVILEGES ON DATABASE <<PROJECT_NAME>>_<<ENVIRONMENT>> TO <<PROJECT_NAME>>_<<ENVIRONMENT>>;
```

If your project has postgres extensions that need to be added, you will need to
do this at the same time.

For example to add the CITEXT extension you would also run on each database in
use for the cluster ('staging', 'production'):

```sql
\connect <<PROJECT_NAME>>_<<ENVIRONMENT>>;
CREATE EXTENSION IF NOT EXISTS citext;
```