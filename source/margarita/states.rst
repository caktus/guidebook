Salt States
===========

SLS files
---------

.. _base:

base
~~~~

Installs packages like `build-essential` and `sudo` that all
our servers need.

No configuration.

.. _elasticsearch:

elasticsearch
~~~~~~~~~~~~~

Adds a repo, installs, and arranges for the service to run at startup
for elasticsearch.

Always adds the elasticsearch-analysis-icu plugin.

Pillar configuration:

* ``elasticsearch_version`` (string):  E.g. '1.7'
* ``elasticsearch_newrelic`` (boolean): Whether to use a newrelic plugin to monitor
  the elasticsearch service in more detail.

Dependencies:

* :ref:`newrelic_npi` (if ``elasticsearch_newrelic`` is True).

.. _fail2ban:

fail2ban
~~~~~~~~

Installs and runs fail2ban.

No configuration.

.. _forward_logs:

forward_logs
~~~~~~~~~~~~

Arranges for all syslog messages to be copied to a remote server
(e.g. Papertrail).

Pillar configuration:

* ``secrets:LOG_DESTINATION`` (string): The host:port to forward the messages to,
  e.g. "log3.example.com:12345".

.. _locale.utf8:

locale.utf8
~~~~~~~~~~~

Sets the system locale, both ``LANG`` and ``LC_ALL``, to ``en_US.UTF-8``.

No configuration.

.. _memcached:

memcached
~~~~~~~~~

Installs and runs memcached.

Leaves all settings and configuration at their defaults.

No configuration.

.. _newrelic_npi:

newrelic_npi
~~~~~~~~~~~~

Install the `New Relic Platform Installer <https://docs.newrelic.com/docs/plugins/plugins-new-relic/installing-plugins/installing-npi-compatible-plugin>`_
that can be used to easily install compatible plugins.

This can be pre-reqed by other states but probably does not need to
be included directly.

No configuration.

.. _newrelic_sysmon:

newrelic_sysmon
~~~~~~~~~~~~~~~

Install and configure the NewRelic monitor for the whole system
(monitors CPU, memory usage, etc.)

Note that if the key is not set in pillar, this state is a no-op, so
it's safe to always include it and then just set the key on the
systems where you want to monitor.

Pillar configuration:

* ``secrets:NEW_RELIC_LICENSE_KEY`` (string): The license key of the New Relic
  account to use.

.. _nginx:

nginx
~~~~~

Install nginx, tweak the default configuration in the main config file,
and remove the default site config that gets installed.

Uses the Nginx PPA to get the latest stable version.

No configuration.

.. _nginx.cert:

nginx.cert
~~~~~~~~~~

Installs (but does not run) a script, ``/var/lib/nginx/generate-cert.sh``,
for creating self-signed certificates for nginx.

Dependencies:

* :ref:`nginx`

No configuration.

.. _nodejs:

nodejs
~~~~~~

Installs node, making sure there's a ``/usr/bin/node`` executable.

No configuration.

.. _postfix:

postfix
~~~~~~~

Install and run postfix mail system.

No configuration.

.. _postgresql:

postgresql
~~~~~~~~~~

Install the configured version of the Postgres database server.  For older
versions, makes sure that UTF-8 locale is the default for the main cluster.
(For newer versions, it comes set up that way.)

Pillar configuration:

* ``postgres_version`` (string): Postgres version to install, e.g. "9.4".

Dependencies:

* :ref:`locale.utf8`

.. _postgresql.client:

postgresql.client
~~~~~~~~~~~~~~~~~

Install the configured version of the Postgres database client.

Pillar configuration:

* ``postgres_version`` (string): Postgres version to install, e.g. "9.4".

No dependencies.

.. _project.cache:

project.cache
~~~~~~~~~~~~~

Open the firewall for memcached from :ref:`app_minions <minions>`.

Dependency on :ref:`memcached` state will also ensure memcached is installed.

Dependencies:

- :ref:`memcached`
- :ref:`ufw`

No configuration.

.. _project.db:

project.db
~~~~~~~~~~

Sets up a project user and database in Postgres.

Updates Postgres server config to accept connections from
:ref:`app_minions <minions>`.

Roles:

* If role is ``db-master`` or ``db-slave``, sets::

    wal_level = hot_standby
    hot_standby = on
    hot_standby_feedback = on
    wal_keep_segments = 128

Pillar configuration:

* ``secrets:DB_PASSWORD`` (string): Password to assign to the project's Postgres user.

The following configuration parameters in postgresql.conf can be
set by putting a corresponding setting under ``postgresql_config``
in Pillar:

* ``max_connections``: default is 100.
* ``shared_buffers``: default is "24MB".
* ``work_mem``: default is "1MB".
* ``maintenance_work_mem``: default is "16MB".
* ``wal_buffers``: default is "-1".
* ``commit_delay``: default is 0.
* ``commit_siblings``: default is 5.
* ``checkpoint_segments``: default is 32
* ``checkpoint_timeout``: default is "10min".
* ``checkpoint_completion_target``: default is '0.9'.
* ``effective_cache_size``: default "128MB".
* ``log_min_duration_statement``: default "250ms".

The following parameters can be set the same way, but are ignored
unless the role is ``db-master`` or ``db-slave``:

* ``max_wal_senders``: default is '0'

Dependencies:

- :ref:`postgresql`
- :ref:`ufw`

.. _project.devs:

project.devs
~~~~~~~~~~~~

Create local users on the server and give them ssh access.

Pillar configuration:

Create a ``users`` dictionary in the pillar. Each dictionary key
should be a username. The value of that dictionary should be another
dictionary, with one key ``public_key`` containing a list, each entry
of which is a public SSH key for that user.  (Paste it in from their
public key file, one long line.)  E.g.::

    users:
      user1:
        public_key:
          - ssh-rsa ADFSDFSDFDFSDFSDF....DFSDFSDFSDF
      user2:
        public_key:
          - ssh-rsa DFSUDFJSDJFSDJKF...SDFJSDKFSDF

Dependencies:

- :ref:`users.groups`

.. _project.dirs:

project.dirs
~~~~~~~~~~~~

Arrange for the project's main directories to be created, e.g.
``/var/www/<project_name>``,
``/var/www/<project_name>/log``,
``/var/www/<project_name>/ssh``, and
``/var/www/<project_name>/services``.

Directories are owned by the project user.

Pillar configuration:

* ``project_name`` (string): Used to construct the paths.

Dependencies:

- :ref:`project.user`

.. _project.django:

project.django
~~~~~~~~~~~~~~

Creates a ``manage.sh`` file in the project directory that invokes
the Django management tool with the right settings.

Depends on other sls files that also do Django-related setup.

Dependencies:

- :ref:`project.user`
- :ref:`project.dirs`
- :ref:`project.venv`

No configuration.

.. _project.queue:

project.queue
~~~~~~~~~~~~~

Arrange for rabbitmq server to be installed and run.

Create rabbitmq user named ``<project_name>_<environment>``, with
password ``BROKER_PASSWORD`` from secrets.

Open the firewall for rabbitmq access to other :ref:`app_minions <minions>` servers.

Pillar configuration:

* ``secrets:BROKER_PASSWORD``: (string) The password to set on the rabbitmq user.
* ``project_name`` (string)

Dependencies:

- :ref:`rabbitmq`
- :ref:`ufw`

.. _project.repo:

project.repo
~~~~~~~~~~~~

Checks out the appropriate version of the project source code to
``/var/www/<project_name>/source``.  Or if environment is ``local``,
rsyncs from the current local directory to the source dir on vagrant.

Create the ``/var/www/<project_name>/source/.env`` file containing all
the environment settings needed to run the project.

Create a wrapper script ``/var/www/<project_name>/source/dotenv.sh``
that sets up the environment from ``.env`` then runs another command.
E.g.::

    cd /var/www/project
    source/dotenv.sh env/bin/python source/manage.py shell

Note that any pillar variable you create inside the ``env`` dictionary or the ``secrets`` dictionary
will be added to the ``.env`` file and the ``dotenv.sh`` script. Both gunicorn and celery are
launched with the ``dotenv.sh`` wrapper, so all of those variables will be available as environment
variables to all of the web and worker processes.

Pillar configuration:

* ``github_deploy_key`` (string): Optional, contains text of the Github deploy key
  to use to access the repository.
* ``repo:url`` (string): Git repository URL
* ``branch`` (string): Branch to check out. Optional; the default is ``master``.
* ``project_name`` (string)

Dependencies:

- :ref:`project.dirs`
- :ref:`project.user`
- :ref:`version-control`
- :ref:`sshd.github`

.. _project.user:

project.user
~~~~~~~~~~~~

Create a local user named ``<project_name>`` and add it to the
``www-data`` group.

Pillar configuration:

* ``project_name`` (string)

.. _project.venv:

project.venv
~~~~~~~~~~~~

Create a virtualenv for the project (at ``/var/www/<project_name>/env``)
and install Python requirements listed in ``requirements_file``. By default,
requirements will be installed from
``/var/www/<project_name>/source/requirements/dev.txt`` if the
environment is ``local``, and otherwise from ``production.txt``.

If a New Relic key is configured, ensures the ``newrelic`` agent package
is installed in the virtual env.

.. note::

    This also installs ``ghostscript``, even though :ref:`python` already does that.
    We should fix that.

Pillar configuration:

* ``project_name`` (string)
* ``python_version`` (string): version of python to use
* ``requirements_file`` (string): path to the project requirements file
  (relative to the project root)

Dependencies:

- :ref:`project.dirs`
- :ref:`project.repo`
- :ref:`python`

.. _project.web.app:

project.web.app
~~~~~~~~~~~~~~~~

Arranges for gunicorn to run the Django server, and for running deploy-time
commands like ``collectstatic`` and ``migrate``.

Pillar configuration:

* ``project_name``
* ``less_version``: What version of the LESS CSS compilation tool to install.

Dependencies:

- :ref:`supervisor.pip`
- :ref:`project.dirs`
- :ref:`project.venv`
- :ref:`project.django`
- :ref:`postfix`
- :ref:`ufw`
- :ref:`nodejs`

.. _project.web.balancer:

project.web.balancer
~~~~~~~~~~~~~~~~~~~~

Arranges for nginx to serve static files for the project and to proxy
other requests to the gunicorn servers.

Set ``letsencrypt: true`` in the pillar configuration, and remove any
``ssl_cert`` and ``ssl_key``, to
use `letsencrypt.org <https://letsencrypt.org>`_ to generate a certificate
that will be trusted by all major browsers, and to renew it periodically.
But this can only work if there's a single web server and the domain points
directly at it. (You might still be able to use `letsencrypt` some other way.)

If you wish to use `letsencrypt` with multiple domain names, add a list
of domains under ``letsencrypt_domains`` in the pillar configuration. (If you
do not set this parameter, letsencrypt defaults to using your pillar config's
`domain` property.)

Note: to switch to letsencrypt from another certificate, it should be
enough to set ``letsencrypt`` and ``admin_email``, remove ``ssl_key`` and
``ssl_cert``, and deploy again.
But the reverse is not true: if you want to switch from letsencrypt
to any other type of certificate, you'll want to manually remove the
symbolic links in ``/var/www/project_name/ssl/`` before turning off
letsencrypt and running another deploy. Otherwise the new cert will
get copied to the symbolic links, which will overwrite the
letsencrypt certs stored in ``/etc/letsencrypt``, which will lead to
very confusing behavior if you ever try to switch back to
letsencrypt.

If you already have a certificate you want to use, you can provide it
in the pillar configuration; see below.

If ``letenscrypt`` is not set and either a key or certificate are not
provided, the deploy will generate and use a self-signed key.

Summary of which certificates will be used:

* If ``ssl_key`` and ``ssl_cert`` are provided, they will be used.
* Otherwise, if ``letsencrypt`` is true, letsencrypt will be used.
* Otherwise, a self-signed certificate will be used.

The nginx configuration redirects non-SSL requests to the corresponding
`https` URL, and sets the ``Strict-Transport-Security`` header to a
very long time.

This state can also set up basic Auth for a site if ``http_auth`` is set
(see configuration below).

If there are multiple hosts with the `web` role, then each nginx
will be configured to proxy requests to Django workers on all the
`web` hosts. I guess if we didn't put a load balancer in front of our
web servers, we could just point our DNS at one of
them and it would spread the load across all of them.

Pillar configuration:

* ``http_auth`` (dictionary): If provided, turn on HTTP Basic Auth on the site,
  and set up a password file for access using each key in the dictionary as a username
  and each corresponding value as that user's password.
* ``domain`` (string): The web server, and if relevant the SSL certificate, will
  be configured to use this domain name.
* ``letsencrypt`` (boolean): If True, use `letsencrypt.org <https://letsencrypt.org>`_
  to get a certificate.
* ``letsencrypt_domains`` (list): List of domain names. We'll request SSL certs for
  each domain name in this list. If this is empty or not set, we'll use ``domain``.
* ``admin_email`` (email address): If ``letsencrypt`` is true, this is required to
  provide an email address for `letsencrypt.org <https://letsencrypt.org>`_ to use.
  This should be a dev team group email address, not an individual's email address.
  This address does not need to be in the site's domain.
* ``ssl_key`` (string): Contents of the SSL key to use.
* ``ssl_cert`` (string): Contents of the SSL certificate to use.
* ``dhparam_numbits`` (integer): How many bits to use when generating the DHE
  parameters. (optional, default 2048).  Generating the DHE file is a one-time
  task, so changing this parameter after it's been generated will have no effect
  unless you manually remove ``/var/www/<project_name>/ssl/dhparams.pem``
  first.

Dependencies:

- :ref:`nginx`
- :ref:`nginx.cert`
- :ref:`ufw`
- :ref:`project.dirs`

.. _project.worker.beat:

project.worker.beat
~~~~~~~~~~~~~~~~~~~~

Arrange for ``celery beat`` service to run for the project via supervisor.

Pillar configuration:

* ``project_name``

Dependencies:

- :ref:`supervisor.pip`
- :ref:`project.dirs`
- :ref:`project.venv`

.. _project.worker.default:

project.worker.default
~~~~~~~~~~~~~~~~~~~~~~

Arrange for a ``celery worker`` service to run for the project via supervisor.
The default worker-specific command-line arguments set log level to ``INFO``.

Pillar configuration:

* ``project_name``
* ``celery_worker_arguments`` (string): Optional, overrides default worker-specific
  command-line arguments.

Dependencies:

- :ref:`supervisor.pip`
- :ref:`project.dirs`
- :ref:`project.venv`
- :ref:`postfix`

.. _python:

python
~~~~~~

Installs the version of python specified in Pillar as ``python_version``, along with a variety of
dev libraries like ``libjpeg8-dev`` that are needed to install various Python packages like Pillow,
as well as setuptools, pip, and virtualenv. You can manually specify additional header packages that
are needed by adding them as a list in the ``python_headers`` pillar variable. This state also makes
a few symlinks that help with building Pillow on 64bit systems.

If you are using Python 2.7, you can set ``python_backport`` to ``True`` which will enable the
Python 2.7.9+ backport for network security enhancements. See
https://www.python.org/dev/peps/pep-0466/. This setting has no effect if you are not using Python
2.7.

(If you're wondering why it installs Ghostscript, that too is required
by some of the imaging tools we sometimes install.)

Pillar configuration:

* ``python_version`` (string)
* ``python_backport`` (Boolean)
* ``python_headers`` (list) List of additional apt packages to be installed.

.. _rabbitmq:

rabbitmq
~~~~~~~~

Install rabbitmq and make it run.

Delete the default ``guest`` rabbitmq user.

No configuration.

.. _redis-master:

redis-master
~~~~~~~~~~~~

Install redis server and make it listen on localhost only.

No configuration or dependencies.

.. _salt.master:

salt.master
~~~~~~~~~~~

Opens ports 4505 and 4506.

Dependencies:

- :ref:`ufw`

No configuration.

.. _solr:

solr
~~~~

Installs ``openjdk-7-jre-headless``.

No configuration.

.. _solr.project:

solr.project
~~~~~~~~~~~~

Installs Solr and copies the default stopwords file into its
configuration.

Does not appear to arrange to run it.

Dependencies:

- :ref:`solr`

No configuration.

.. _sshd:

sshd
~~~~

Install and run openssh client and server.

Configure ssh server, disabling root login, and restricting access
so only users in the ``login`` group may ssh into the server.

Opens port 22.

Dependencies:

- :ref:`ufw`
- :ref:`fail2ban`

No configuration.

.. _sshd.github:

sshd.github
~~~~~~~~~~~

Add ``github.com`` to the system known hosts file.

No configuration.

.. _statsd:

statsd
~~~~~~

Install statsd and provide basic default configuration, arranging
for it to run on startup.

Dependencies:

- :ref:`nodejs`
- :ref:`version-control`

No configuration.

.. _syslog:

syslog
~~~~~~

Arrange to install rsyslog v8.5 or later.

Configure it to load the `imfile` module so that other states
can add rsyslog config files to tell rsyslog to monitor plain
text log files.

No configuration.

.. _sudo:

sudo
~~~~

Arrange for sudo service to run.

Update the ``sudoers`` config file to let users in group ``admin``
do anything without a password.

No configuration.

.. _supervisor:

supervisor
~~~~~~~~~~

.. deprecated:: forever
  Use ``supervisor.pip`` instead.

Install and run supervisor using its Debian/Ubuntu package.

No configuration.

.. _supervisor.pip:

supervisor.pip
~~~~~~~~~~~~~~

Install and run supervisor after installing it globally using
``pip``, first uninstalling the packaged supervisor if necessary.

.. _ufw:

ufw
~~~~

Install the ``ufw`` firewall package and set it to deny access
by default.

No configuration.

.. _unattended_upgrades:

unattended_upgrades
~~~~~~~~~~~~~~~~~~~

Arrange for ``apt`` to install security updates weekly and
notify someone of the results.

Regardless of the configuration, will never update any ``salt-*``
packages.

Pillar configuration:

* ``admin_email`` (string): Required; email address to send notifications of
  the update results to
* ``unattended_upgrade_blacklist`` (list of strings and regexes): Optional package name
  not to ever upgrade this way. Can include both exact names of packages and regexes
  that match package names.

Dependencies:

- :ref:`syslog`

.. _users.groups:

users.groups
~~~~~~~~~~~~

Create system user groups named ``admin`` and ``login``.

No configuration.

.. _vagrant.user:

vagrant.user
~~~~~~~~~~~~

Add the ``vagrant`` user to the ``admin`` and ``login`` groups so that
with our updated configuration for ``ssh`` and ``sudo``, the vagrant user
can still login and do things as root.

Dependencies:

- :ref:`users.groups`

No configuration.

.. _version-control:

version-control
~~~~~~~~~~~~~~~

Install git, mercurial, and subversion.

No configuration.
