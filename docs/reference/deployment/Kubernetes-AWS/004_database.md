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
