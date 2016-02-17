Interface between the deploy system and projects
================================================

This interface isn't always as clear-cut as it could be. For now, we'll
try to document it as-is.

Definitions
~~~~~~~~~~~

`Project`: One or more sites that share a code base. In other words,
if sites' Django code comes from the same source control repository,
we'll call them part of the same project.  The Twelve-Factor App `calls
this the app <http://12factor.net/codebase>`_.

`Environment`: A configuration and set of one or more systems that
make the project available on the network with a unique domain and
set of data.  For example, we might have testing, staging,
and production environments.

The Twelve-Factor app `calls these deploys <http://12factor.net/config>`_.

`Instance`: In at least one case, we've run a project on one domain
with multiple independent sets of user accounts and data (accessed
at different URLs under the domain). We refer to each of those as
an instance. Sometimes this is refered to as `multitenancy`.

`Role`: Each system in an environment plays one or more roles, meaning
that it provides some service to the environment. Example roles include
database master, web server, celery worker, cache, etc.

`Configuration variable`: Any piece of information that needs to be
provided to the code at runtime.  Example: the database server hostname, or the
environment name.  See also
`the Twelve-Factor App: configuration <http://12factor.net/config>`_.

The Twelve-Factor App principles say we shouldn't have these checked
into source control, but we typically do that, sometimes using a separate
repository for the deploy-related files, and encrypting the secrets. It's
still a good way to manage this information. Maybe someday we'll move to
something like Consul.

`Secret`: A configuration variable that must not be exposed
to the public or we risk compromising our sites. Secrets typically
include passwords, access keys, Django's secret key setting, etc.

Directories
~~~~~~~~~~~

For most projects, we create ``/var/www/<projectname>``, with subdirectories
for the virtual environment, code, logs, ssl files, etc.

Python Dependencies
~~~~~~~~~~~~~~~~~~~

The deploy system will set up a virtual environment and use it to
run the Django processes of the project.

The file ``requirements/production.txt`` from the code is used to
``pip install`` the project's dependencies into the virtual environment
during the deploy.

Configuration
~~~~~~~~~~~~~

The life of configuration variables
-----------------------------------

1. Configuration variables are stored somehow in our deploy environment.
   Right now, that's in Salt pillar data, with secrets grouped into a
   ``secrets`` dictionary and protected by
   `encryption <https://docs.saltstack.com/en/latest/ref/renderers/all/salt.renderers.gpg.html>`_.

2. The deploy process creates a ``.env`` file in the root of the
   deployed code on each server, containing the appropriate values
   of the configuration variables for that server.  The file is only
   readable by the project user.

3. When ``manage.py`` or ``wsgi.py`` starts, it reads ``.env`` and
   sets all the specified environment variables. (This is a modification
   of the standard Django versions of these files.)

4. Django uses the DJANGO_SETTINGS_MODULE environment variable
   to control which settings file is used.

5. The settings file looks at the environment variables to find out
   configuration variables' values.

Scopes of configuration variables
---------------------------------

It's the nature of configuration variables that some are the same
across the whole project (project name, where the code repository is,
what version of Python the project needs to run on),
while others might be different from one environment to another
(environment name, domain, database).

In our Salt-based deploy system, we manage this by having separate
``.sls`` files providing Pillar data for the entire project and for
each environment, and including the right ones from the
pillar ``top.sls`` file.

Deploy settings
---------------

These are some settings that the deploy system looks at, but that
are not (necessarily) needed by Django.  They're still passed to Django
as environment variables in case the Django app wants to use them, though.

  * elasticsearch_newrelic: true to enable New Relic monitoring of Elastic Search servers
  * environment: The name of the deploy environment; must be a valid identifier.
    E.g. "testing" or "production".
  * github_deploy_key: Used to checkout private repositories from Github, if needed. (secret)
  * LOG_DESTINATION: where to forward system logs to, e.g. "host.example.com:1234". (secret)
  * postgres_version: The PostgreSQL version to use, e.g. "9.3".
  * project_name: The name of the project; must be a valid identifier.
  * python_version: The Python version to use, e.g. "3.4".
  * repo.url: The Git repo URL to get the code from.
  * repo.branch: The Git branch or commit name to check out.
  * ssl_key and ssl_cert: If both provided, they provide the SSL certificate and key to use. Otherwise, a self-signed
    certificate is used, generating a new one if needed.
  * users: A list of usernames to create and the SSH public keys to give access to them
    (typically used to give developers access to the servers for deploys, debugging, etc.).

Django settings
---------------

Here are the environment variables that the Django settings file
should look at for configuration values:

  * BROKER_HOST: hostname where RabbitMQ is running
  * BROKER_PASSWORD: password for the RabbitMQ user. (secret)
  * CACHE_HOST: hostname where memcache is running
  * DB_HOST: hostname of database server (optional; use localhost otherwise)
  * DB_PORT: port of database server (optional; use default Postgres port 5432 otherwise)
  * DB_PASSWORD: password for database user. (secret)
  * DOMAIN: hostname from the site's URL
  * ENVIRONMENT: name of the environment
  * NEW_RELIC_LOG: e.g. "/var/log/newrelic/agent.log"
  * NEW_RELIC_APP_NAME: e.g. "myproject <environment>"
  * NEW_RELIC_LICENSE_KEY: This is the license key for the New Relic account to use for monitoring.
    If provided, turn on New Relic monitoring. (secret)
  * NEW_RELIC_MONITOR_MODE: "true" or "false"
  * SECRET_KEY: the Django SECRET_KEY. (secret)

Projects always assume a database username, database name, and broker username of
``<projectname>_<lowercased envname>``.

ALLOWED_HOSTS is set to ``[DOMAIN]``.
