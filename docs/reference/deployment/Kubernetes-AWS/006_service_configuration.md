# Configure Services

The configuration of services for your deployment will occur almost entirely in the `deploy/group_vars/all.yaml` file.

## Global

```yaml
# ----------------------------------------------------------------------------
# Global: CloudFormation stack outputs. See all.yml for stack parameters.
# ----------------------------------------------------------------------------

ClusterEndpoint: <ClusterEndpoint from CloudFormation output>
DatabaseAddress: <DatabaseAddress from CloudFormation output>  # The connection endpoint for the database. -
RepositoryURL: <DIGITS>.dkr.ecr.<ACCOUNT_REGION>.amazonaws.com  # The docker repository URL
```

The output for `RepositoryURL` is in two parts the first part is up to the first `/`. Copy that into `RepositoryURL`.
The second part goes in `k8s_container_image` under [App Pod Configuration](#app-pod-configuration)


## App Pod Configuration


```yaml
# ----------------------------------------------------------------------------
# App Pod Configuration
# ----------------------------------------------------------------------------
...Defaults

k8s_container_image: "{{ RepositoryURL }}/<SECOND_PART_OF_REPOSITORY_URL>"

...End Defaults
```

## Shared Environment Variables

Shared variables is a section in the `k8s.yaml` file where you can configure some items that
would most likely be shared between all of your environments.

Variables in this section are also prefixed with `env_`, this usually indicates that they will be 
used by Django or something else in the app.

```yaml
# ----------------------------------------------------------------------------
# Shared Environment Variables
# ----------------------------------------------------------------------------
env_database_url: "postgres://{{ django_app_name }}_{{ env_name }}:{{ database_password }}@{{ DatabaseAddress }}:5432/{{ django_app_name }}_{{ env_name }}"
env_django_settings: "{{ django_app_name }}.settings.deploy"
env_cache_host: memcached:11211
env_default_file_storage: "DjangoFileSystem"

env_media_storage_bucket_name: ""
env_aws_default_acl: public-read
env_media_location: "{{ env_name }}/media/"

# Email
env_email_host: 
env_email_host_user: 
env_email_host_password: 
env_default_from_email: 

env_default_from_email# New Relic APM: Caktus Free Account
env_new_relic_app_name: "{{ k8s_namespace }}"
env_new_relic_license_key: 
env_sentry_dsn:
```
