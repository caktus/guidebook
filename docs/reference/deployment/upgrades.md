# Kubernetes Upgrades

Caktus routinely performs Kubernetes and related service upgrades as part of our hosting services.

## Hotfix branch 

Upgrades are rolled out to production environments, so create a [hotfix](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) branch:

```sh
git checkout main
git pull
git checkout -B k8s-upgrades
```

## Ingress controller and cert-manager

### Pin to latest versions

Update `k8s_ingress_nginx_chart_version` and `k8s_cert_manager_chart_version` to the target versions, typically in `deploy/group_vars/k8s.yaml`:

```yaml
k8s_ingress_nginx_chart_version: "4.0.19"
k8s_cert_manager_chart_version: "v1.7.2"
```

### Deploy the upgrades

```sh
# using kubesae
inv deploy.install deploy.playbook deploy-cluster.yml
```

#### Troubleshooting

If any Ansible tasks fail to run, check for a **failed** status of the Helm charts in the respective namespaces:

```sh
helm -n ingress-nginx list
helm -n cert-manager list
```

Rollback and re-deploy as needed. For example, **cert-manager**:

```sh
helm -n cert-manager rollback cert-manager
inv deploy.install deploy.playbook deploy-cluster.yml
```

## Re-deploy app

Find environment namespaces:

```sh
kubectl get ns
```

### Staging

Find deployed tag:

```sh
kubectl -n trafficstops-staging get deploy/app -o yaml | grep image:
```

Re-deploy:

```sh
inv staging deploy --tag=<insert tag here>
```

### Production

Repeate these steps for the production namespace.

## Hosting Services

This section manages database backups, monitoring, and log aggregation.


### Update Galaxy requirements

Update [caktus.k8s-hosting-services](https://github.com/caktus/ansible-role-k8s-hosting-services) to the latest version in `deploy/requirements.yml`:

```yaml
- src: https://github.com/caktus/ansible-role-k8s-hosting-services
  name: caktus.k8s-hosting-services
  version: v0.7.0
```

### Update chart versions

Update the hosting services chart versions to the target versions, typically in `deploy/group_vars/k8s.yaml`:

```yaml
# https://github.com/newrelic/helm-charts/releases
k8s_newrelic_chart_version: "4.6.2"
# https://hub.docker.com/r/gliderlabs/logspout/tags
k8s_papertrail_logspout_image_tag: v3.2.14
```

### Deploy

Run the `deploy-hosting-services.yml` to deploy the latest hosting services:

```sh
inv deploy.install deploy.playbook deploy-hosting-services.yml
```

## Commandline updates for AWS EKS
This command updates an EKS cluster
```sh
aws eks update-cluster-version --region <AWS Region> --name <cluster name> --kubernetes-version <K8s version to update to>
```

This command uses the update-id from the update-cluster-version command to list the status of the upgrade 
```sh
aws eks describe-update --region <AWS Region> --name <cluster name> --update-id <update-ID from update command>  | grep "status"
```
