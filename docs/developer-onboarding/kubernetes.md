# Kubernetes

The current Caktus Kubernetes version target is **v1.22** for projects under Hosting Services.


## Install kubectl

The Kubernetes command-line tool, kubectl, allows you to run commands against
Kubernetes clusters. 

kubectl is installable on a
[variety of platforms](https://kubernetes.io/docs/tasks/tools/). See [Patch Releases](https://kubernetes.io/releases/patch-releases/) for the lastest release versions. Follow the instructions below to install kubectl.


### Apple Silicon (ARM)

```shell
curl -LO "https://dl.k8s.io/release/v1.22.9/bin/darwin/arm64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

### Apple Intel (x86)

```shell
curl -LO "https://dl.k8s.io/release/v1.22.9/bin/darwin/amd64/kubectl"
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl
```


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
