# Configure Services

The configuration of services for your deployment will occur almost entirely in the `deploy/group_vars/all.yaml` file.

## Global

```yaml
# ----------------------------------------------------------------------------
# Global: CloudFormation stack outputs. See all.yml for stack parameters.
# ----------------------------------------------------------------------------

ClusterEndpoint: <ClusterEndpoint from CloudFormation output>
DatabaseAddress: <DatabaseAddress from CloudFormation output>  # The connection endpoint for the database. -
RepositoryURL: <<DIGITS>.dkr.ecr.<ACCOUNT_REGION>.amazonaws.com  # The docker repository URL
```

The output for `RepositoryURL` is in two parts the first part is up to the first `/`. Copy that into `RepositoryURL`.
The second part goes in `k8s_container_image` under [App Pod Configuration](#app-pod-configuration)

## App Pod Configuration
```yaml
# ----------------------------------------------------------------------------
# App Pod Configuration
# ----------------------------------------------------------------------------
...Defaults

k8s_container_image: "{{ RepositoryURL }}/<SECOND_PART_OF_REPOSITORY_URL"

...End Defaults
```

## 
