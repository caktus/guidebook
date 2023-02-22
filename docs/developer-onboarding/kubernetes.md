# Kubernetes

The current Caktus Kubernetes version target is **v1.22** for projects under Hosting Services.


## Install kubectl

The Kubernetes command-line tool, kubectl, allows you to run commands against
Kubernetes clusters. 

kubectl is installable on a
[variety of platforms](https://kubernetes.io/docs/tasks/tools/). See [Patch Releases](https://kubernetes.io/releases/patch-releases/) for the lastest release versions. Follow the instructions below to install kubectl.


### Apple Silicon (ARM)

```shell
curl -LO "https://dl.k8s.io/release/v1.22.17/bin/darwin/arm64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

### Apple Intel (x86)

```shell
curl -LO "https://dl.k8s.io/release/v1.22.17/bin/darwin/amd64/kubectl"
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl
```


## Helm

Helm is a package manager for Kubernetes and we use various Helm charts at Caktus. To install, follow the instructions below.

Caktus Hosting Services currently recommends this version:

```sh
export HELM_VERSION=3.8.2
```

### Apple Silicon (ARM)

```shell
curl -LO "https://get.helm.sh/helm-v$HELM_VERSION-darwin-arm64.tar.gz"
tar -zxf helm*.tar.gz
mv ./darwin-arm64/helm /usr/local/bin
```

### Apple Intel (x86)

```shell
curl -LO "https://get.helm.sh/helm-v$HELM_VERSION-darwin-amd64.tar.gz"
tar -zxf helm*.tar.gz
mv ./darwin-amd64/helm /usr/local/bin
```

### Linux (x86)

```shell
curl -LO "https://get.helm.sh/helm-v$HELM_VERSION-linux-amd64.tar.gz"
tar -zxf helm*.tar.gz
sudo mv ./linux-amd64/helm /usr/local/bin
```

Verify it's installed correctly. You should see something like this:

```shell
❯ helm version 
version.BuildInfo{Version:"v3.8.1", GitCommit:"5cb9af4b1b271d11d7a97a71df3ac337dd94ad37", GitTreeState:"clean", GoVersion:"go1.17.5"}
```
