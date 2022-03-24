# Kubernetes


## Helm

Helm is a package manager for Kubernetes and we use various Helm charts at Caktus. To install `helm`, follow the [From Script](https://helm.sh/docs/intro/install/#from-script) instructions in docs:

```shell
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

Verify it's installed correctly. You should see something like this:

```shell
❯ helm version 
version.BuildInfo{Version:"v3.8.1", GitCommit:"5cb9af4b1b271d11d7a97a71df3ac337dd94ad37", GitTreeState:"clean", GoVersion:"go1.17.5"}
```
