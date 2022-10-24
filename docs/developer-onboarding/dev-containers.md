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

### Build

Build and run development container:

```sh
docker compose up --build -d
```

### Restore database archive

Restore database from latest production backup:

```sh
docker compose exec django bash
/code# dropdb myproject && createdb myproject
/code# inv utils.get-db-backup
/code# pg_restore -Ox -d $DATABASE_URL < *.pgdump
/code# rm *.pgdump
```

### Sync staging media

Restore media from production S3 bucket:

```sh
/code# inv production aws.sync-media -s local --bucket-path="media/"
```

### Start Development Server(s)

Start your Django development server in Terminal 1:

```sh
docker compose exec django bash
/code# python manage.py runserver 0.0.0.0:8000
```

Start your Node development server in Terminal 2:

```sh
docker compose exec django bash
/code# npm run dev:dashboard
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
