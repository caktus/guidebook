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

### Commandline updates for AWS EKS
This command updates an EKS cluster
```sh
aws eks update-cluster-version --region <AWS Region> --name <cluster name> --kubernetes-version <K8s version to update to>
```

This command uses the update-id from the update-cluster-version command to list the status of the upgrade 
```sh
aws eks describe-update --region <AWS Region> --name <cluster name> --update-id <update-ID from update command>  | grep "status"
```
