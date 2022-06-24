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

TBD

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
