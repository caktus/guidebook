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

* :fontawesome-brands-aws: Caktus AWS account and AWS Command Line Interface (AWS CLI) [configured for your development projects](AWS.md).

* (Optional) [Visual Studio Code](https://code.visualstudio.com/) with the [Remote Development extension pack](https://aka.ms/vscode-remote/download/extension). See [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers) for additional information.

## Project Setup

A project's documentation is the canonical setup documentation. Please refer to your project docs for detailed setup instructions.

However, most projects should roughly follow this pattern:

1. **Build and start dev container:** Using the [VS Code Command Pallete (`⇧⌘P`)](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette), select `Dev Containers: Reopen in Container`.
2. **Setup pre-commit:** Insetall pre-commit to enforce a variety of community standards:
   ```sh
   pre-commit clean
   pre-commit install
   ```
3. **Reset local database:** Download copy of staging database and restore it locally:
   ```sh
   inv aws.configure-eks-kubeconfig
   inv staging pod.get-db-dump
   dropdb --if-exists DATABASENAME && createdb DATABASENAME
   pg_restore -Ox -d $DATABASE_URL < *.dump
   ```
4. **Reset local media:** Download copy of staging media:
   ```sh
   mkdir -p /code/media && sudo chown -R appuser:appuser /code/media
   inv staging aws.sync-media --sync-to local --bucket-path="media/"
   ```
5. **Start dev server:**: Start the Django development server:
   ```sh
   python manage.py runserver 0.0.0.0:8000
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
