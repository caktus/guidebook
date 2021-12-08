Deploying to a Dokku server
===========================

Projects created using a recent version of the Caktus
[django-project-template](https://github.com/caktus/django-project-template)
can be deployed to a Dokku server as follows.

These instructions assume

-   that `ssh dokku` will connect you to your dokku server as the dokku
    user. You can add something like this to your `~/.ssh/config` file
    to achieve that:

        Host dokku
          Hostname dokku.server.example.com
          User dokku

-   the [Postgres plugin](https://github.com/dokku/dokku-postgres) is
    installed on the dokku server (follow link for instructions)
-   the [Lets Encrypt
    plugin](https://github.com/dokku/dokku-letsencrypt) is installed on
    the dokku server (follow link for instructions)
-   an admin has
    [created](http://dokku.viewdocs.io/dokku~v0.11.2/advanced-usage/persistent-storage/)
    a directory on the dokku server named
    `/var/lib/dokku/data/storage/{{ project_name }}` that we can use for
    storage that persists across deploys, and that is writable by the
    `dokku` user. (follow link for instructions)
-   your new project is checked into git (required by dokku). If you
    haven\'t done that, you can cd into the project directory and run:

        $ git init && git add . && git commit -m "Initial commit"

Running:

    ./dokku_first_deploy.sh

from the new project directory will do much of the following. Or you can
go through step-by-step yourself as follows.

Create a new app:

    $ ssh dokku apps:create {{ project_name }}
    Creating {{ project_name }}... done

Mount the persistent storage at `/storage` inside the container, and set
a config variable to tell Django where we\'re going to store our media:

    $ ssh dokku storage:mount {{ project_name }} /var/lib/dokku/data/storage/{{ project_name }}:/storage
    $ ssh dokku config:set {{ project_name }} MEDIA_ROOT=/storage/media MEDIA_URL=/media

Create a database:

    $ ssh dokku postgres:create {{ project_name }}-database
            Waiting for container to be ready
            Creating container database
            =====> Postgres container created: {{ project_name }}-database
            =====> Container Information
                   Config dir:          /var/lib/dokku/services/postgres/{{ project_name }}-database/config
                   Data dir:            /var/lib/dokku/services/postgres/{{ project_name }}-database/data
                   Dsn:                 postgres://postgres:5a7dcf4d92435f287a582de383fc99da@dokku-postgres-{{ project_name }}-database:5432/{{ project_name }}_database
                   Exposed ports:       -
                   Id:                  19f9c4618b80ff500d7ea296993e995b423692c1a05da226f483de654ba3c752
                   Internal ip:         172.17.0.16
                   Links:               -
                   Service root:        /var/lib/dokku/services/postgres/{{ project_name }}-database
                   Status:              running
                   Version:             postgres:9.6.1
    $ ssh dokku postgres:link {{ project_name }}-database {{ project_name }}
            no config vars for test_template
            -----> Setting config vars
                   DATABASE_URL: postgres://postgres:5a7dcf4d92435f287a582de383fc99da@dokku-postgres-test-template-database:5432/test_template_database
            -----> Restarting app test_template
            App test_template has not been deployed

Set a secret key:

    $ ssh dokku config:set {{ project_name }} DJANGO_SECRET_KEY=$(make generate-secret)
            -----> Setting config vars
                   DJANGO_SECRET_KEY: cHDFoeujP9oJkODdxPrXICWM0jBDKyVz
            -----> Restarting app test_template
            App test_template has not been deployed

Set an environment name:

    $ ssh dokku config:set {{ project_name }} ENVIRONMENT=production
    -----> Setting config vars
           ENVIRONMENT: production
    -----> Restarting app test_template
    App test_template has not been deployed

Set the domain name:

    $ ssh dokku config:set {{ project_name }} DOMAIN={{ project_name }}.$(ssh dokku domains:report {{ project_name }} --domains-global-vhosts)
    -----> Setting config vars
           DOMAIN: test_template.caktustest.net
    -----> Restarting app test_template
    App test_template has not been deployed

Deploy:

    $ git remote add dokku dokku:{{ project_name }}
    $ git push dokku master
    Counting objects: 82, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (73/73), done.
    Writing objects: 100% (82/82), 89.87 KiB | 5.99 MiB/s, done.
    Total 82 (delta 2), reused 0 (delta 0)
    -----> Cleaning up...
    -----> Building test_template from herokuish...
    -----> Adding BUILD_ENV to build environment...
    -----> Warning: Multiple default buildpacks reported the ability to handle this app. The first buildpack in the list below will be used.
           Detected buildpacks: multi nodejs python
    -----> Multipack app detected
    =====> Downloading Buildpack: https://github.com/heroku/heroku-buildpack-nodejs.git
    =====> Detected Framework: Node.js

    -----> Creating runtime environment

           NPM_CONFIG_LOGLEVEL=error
           NPM_CONFIG_PRODUCTION=true
           NODE_VERBOSE=false
           NODE_ENV=production
           NODE_MODULES_CACHE=true

    -----> Installing binaries
           engines.node (package.json):  >=4.2 <4.3
           engines.npm (package.json):   unspecified (use default)

           Resolving node version >=4.2 <4.3...
           Downloading and installing node 4.2.6...
           Using default npm version: 2.14.12

    -----> Restoring cache
           Loading 2 from cacheDirectories (default):
           - node_modules (not cached - skipping)
           - bower_components (not cached - skipping)

    -----> Building dependencies
           Installing node modules (package.json)

    -----> Caching build
           Clearing previous node cache
           Saving 2 cacheDirectories (default):
           - node_modules (nothing to cache)
           - bower_components (nothing to cache)

    -----> Build succeeded!
    =====> Downloading Buildpack: https://github.com/heroku/heroku-buildpack-python.git
    =====> Detected Framework: Python
           !     The latest version of Python 3 is python-3.6.2 (you are using python-3.6.3, which is unsupported).
           !     We recommend upgrading by specifying the latest version (python-3.6.2).
           Learn More: https://devcenter.heroku.com/articles/python-runtimes
    -----> Installing python-3.6.3
    -----> Installing pip
    -----> Installing requirements with pip

    ...

           Successfully installed BeautifulSoup4-4.4.0 Django-1.8.18 Pillow-2.9.0 dealer-2.0.5 dj-database-url-0.4.2 django-dotenv-1.3.0 gunicorn-19.7.1 psycopg2-2.6.1 python3-memcached-1.51 six-
    1.9.0 whitenoise-3.3.0

    -----> $ python manage.py collectstatic --noinput
           67 static files copied to '/tmp/build/www/public/static', 67 post-processed.

           Using release configuration from last framework (Python).
    -----> Discovering process types
           Procfile declares types -> web
    -----> Releasing test_template (dokku/test_template:latest)...
    -----> Deploying test_template (dokku/test_template:latest)...
    -----> Attempting to run scripts.dokku.predeploy from app.json (if defined)
    -----> Running 'python manage.py migrate --noinput' in app container
           restoring installation cache...
           Operations to perform:
             Synchronize unmigrated apps: staticfiles, sitemaps, messages, humanize, runserver_nostatic
             Apply all migrations: sessions, admin, auth, contenttypes
           Synchronizing apps without migrations:
             Creating tables...
               Running deferred SQL...
             Installing custom SQL...
           Running migrations:
           ...
           removing installation cache...
    -----> App Procfile file found (/home/dokku/test_template/DOKKU_PROCFILE)
    -----> DOKKU_SCALE file not found in app image. Generating one based on Procfile...
    -----> New DOKKU_SCALE file generated
    =====> web=1
    -----> Attempting pre-flight checks
           For more efficient zero downtime deployments, create a file CHECKS.
           See http://dokku.viewdocs.io/dokku/deployment/zero-downtime-deploys/ for examples
           CHECKS file not found in container: Running simple container check...
    -----> Waiting for 10 seconds ...
    -----> Default container check successful!
    -----> Running post-deploy
    =====> renaming container (dca40bf8f34e) nostalgic_yalow to test_template.web.1
    -----> Creating new /home/dokku/test_template/VHOST...
    -----> Setting config vars
           DOKKU_NGINX_PORT: 80
    -----> Setting config vars
           DOKKU_PROXY_PORT_MAP: http:80:5000
    -----> Configuring test_template.caktustest.net...(using built-in template)
    -----> Creating http nginx.conf
    -----> Running nginx-pre-reload
           Reloading nginx
    -----> Setting config vars
           DOKKU_APP_RESTORE: 1
    -----> Attempting to run scripts.dokku.postdeploy from app.json (if defined)
    =====> Application deployed:
           http://test_template.caktustest.net

    To dokku:test_template
     * [new branch]      master -> master

Notice that when the deploy finishes, the application\'s URL is shown.

Now that the application is running on port 80, we can add SSL:

    $ ssh dokku letsencrypt ssh dokku config:set --no-restart {{ project_name }} DOKKU_LETSENCRYPT_EMAIL=your@email.tld
    $ ssh dokku letsencrypt {{ project_name }}
    $ ssh dokku letsencrypt:cron-job --add {{ project_name }}

See the [Dokku deployment
documentation](http://dokku.viewdocs.io/dokku/deployment/application-deployment/)
and the rest of the Dokku documentation for more details.

Backups
-------

To backup the database and media, first download a dump of the database
somewhere:

    $ ssh dokku postgres:export {{ project_name }}-database > somefile.dump

Then backup the dump and the storage directory:

    $ some_backup_command somefile.dump /var/lib/dokku/data/storage/{{ project_name }}
