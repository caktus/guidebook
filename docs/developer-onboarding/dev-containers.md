# Development Containers

Development containers provide a local environment setup option for Mac and Linux at Caktus. Alternatively, if you'd prefer a more customized experience, you'll likely want to follow the general [Developer On-boarding](index.md) docs instead.

## Goals

Development containers will:

* Use the same Python/Node/etc. versions as the deployed environment.
* Install base and development Python/Node/etc. packages automatically without having to use homebrew, pyenv, nvm, etc.
* Streamline database and media sync from staging environments to ease initial setup.
* Provide aws-cli and kubectl tools so you can access deployed environments.
* Allow Git pull, commit, and push from within the container if using VS Code devcontainer.

## Prerequisites

To get started, make sure you have:

* Git and SSH keys configured as documented in [Generating a new SSH key](M1.md#generating-a-new-ssh-key).

* :fontawesome-brands-docker: Container runtime like [Docker Desktop on Mac](https://docs.docker.com/desktop/install/mac-install/) or [Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

    * [BuildKit enabled](https://docs.docker.com/develop/develop-images/build_enhancements/) to support features provided by BuildKit builder toolkit.

    !!! info "Quirks with local filesystem (bind) mounts on Linux :fontawesome-brands-linux:"

        Inside a container on Linux, any mounted files/folders will have the exact same permissions as outside the container - including the owner user ID (UID) and group ID (GID). Because of this, your container user will either need to have the same UID or be in a group with the same GID. **If your user does not have a UID of 1000** (run `id` in your terminal to check), then you should specify `USER_UID` and `USER_GID` in a `.env` file at the root of your repo:
        
        ```sh
        USER_UID=1001
        USER_GID=1001
        ```
        
        See [Add a non-root user to a container](https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user) for more information.

* :fontawesome-brands-aws: Caktus AWS account and AWS Command Line Interface (AWS CLI) [configured for your development projects](AWS.md).

* (Optional) [Visual Studio Code](https://code.visualstudio.com/) with the [Remote Development extension pack](https://aka.ms/vscode-remote/download/extension). See [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers) for additional information.

!!! warning ":material-apple: Apple Silicon (M1/M2) and VS Code Live Share"

    VS Code Live Share's `vsls-agent` does not support M1/arm64 yet, so Apple Silicon users cannot start a share from within a Dev Container. See [MicrosoftDocs/live-share#4060](https://github.com/MicrosoftDocs/live-share/issues/4060) for more information.
    
    However, Apple Silicon users can start a Live Share session outside of a Dev Container and use `docker compose exec django` to run commands.

## Project Setup

A project's documentation is the canonical setup documentation. Please refer to your project docs for detailed setup instructions.

However, most projects should roughly follow this pattern:

1. **Build and start dev container:** Using the [VS Code Command Pallete (`⇧⌘P`)](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette), select `Dev Containers: Reopen in Container`.
2. **Install Python and Node requirements:** 
   ```sh
   python3 -m venv /code/venv
   make setup
   npm install
   ```
3. **Setup pre-commit:** Insetall pre-commit to enforce a variety of community standards:
   ```sh
   pre-commit clean
   pre-commit install
   ```
4. **Reset local database:** Download copy of staging database and restore it locally:
   ```sh
   inv aws.configure-eks-kubeconfig
   inv staging pod.get-db-dump
   dropdb --if-exists DATABASENAME && createdb DATABASENAME
   pg_restore -Ox -d $DATABASE_URL < *.dump
   ```
6. **Reset local media:** Download copy of staging media:
   ```sh
   mkdir -p /code/media && sudo chown -R appuser:appuser /code/media
   inv staging aws.sync-media --sync-to local --bucket-path="media/"
   ```
7. **Start dev server:**: Start the Django development server:
   ```sh
   python manage.py runserver 0.0.0.0:8000
   ```
7. **Start Node dev server:** Start the Node development server in a separate terminal:
   ```sh
   npm run dev
   ```

## Troubleshooting

### `Bad configuration option: usekeychain`

If you're on a Mac, you may see an error like this:

```sh
/home/appuser/.ssh/config: line 3: Bad configuration option: usekeychain
/home/appuser/.ssh/config: terminating, 1 bad configuration options
fatal: Could not read from remote repository.
```

This is due to a special config option available on the Mac ssh-agent. To allow the dev container ssh-agent to ignore it, add this line to the top of `~/.ssh/config`:

```config
IgnoreUnknown AddKeysToAgent,UseKeychain
```
