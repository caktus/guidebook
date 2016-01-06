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

.. _memcached:

memcached
~~~~~~~~~

Installs and runs memcached.

Leaves all settings and configuration at their defaults.

.. _newrelic_npi:

newrelic_npi
~~~~~~~~~~~~

Install the `New Relic Platform Installer <https://docs.newrelic.com/docs/plugins/plugins-new-relic/installing-plugins/installing-npi-compatible-plugin>`_
that can be used to easily install compatible plugins.

This can be pre-reqed by other states but probably does not need to
be included directly.

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

.. _nginx.cert:

nginx.cert
~~~~~~~~~~

Installs (but does not run) a script, ``/var/lib/nginx/generate-cert.sh``,
for creating self-signed certificates for nginx.

Dependencies:

* :ref:`nginx`

.. _nodejs:

nodejs
~~~~~~

Installs node, making sure there's a ``/usr/bin/node`` executable.

.. _postfix:

postfix
~~~~~~~

Install and run postfix mail system.

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

.. _project.cache:

project.cache
~~~~~~~~~~~~~

Open the firewall for memcached from :ref:`app_minions <minions>`.

Dependency on `memcached` state will also ensure memcached is installed.

Dependencies:

- :ref:`memcached`
- :ref:`ufw`

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

.. _project.queue:

project.queue
~~~~~~~~~~~~~

Arrange for rabbitmq server to be installed and run.

Create rabbitmq user named ``<project_name>_<environment>``, with
password BROKER_PASSWORD from secrets.

Open the firewall for rabbitmq access to other :ref:`app_minions <minions>` servers.

Pillar configuration:

* ``secrets:BROKER_PASSWORD``: The password to set on the rabbitmq user.

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

Pillar configuration:

* ``github_deploy_key`` (string): Optional, contains text of the Github deploy key
  to use to access the repository.
* ``repo:url`` (string): Git repository URL
* ``repo:branch`` (string): Branch to check out. Optional; default is ``master``.

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

.. _project.venv:

project.venv
~~~~~~~~~~~~

Create a virtualenv for the project (at ``/var/www/<project_name>/env``)
and install Python requirements listed in
``/var/www/<project_name>/source/requirements/dev.txt`` if the
environment is ``local``, and otherwise from ``production.txt``.

Also installs ``ghostscript`` ?!?!?!

Dependencies:

- :ref:`project.dirs`
- :ref:`project.repo`
- :ref:`python`

.. _project.web.app:

project.web.app
~~~~~~~~~~~~~~~~

Arranges for gunicorn to run the Django server, and for running deploy-time
commands like ``collectstatic`` and ``migrate``.

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

If either a key or certificate are not provided, will generate and use
a self-signed key.

Pillar configuration:

* ``http_auth`` (dictionary): If provided, turn on HTTP Basic Auth on the site,
  and set up a password file for access using each key in the dictionary as a username
  and each corresponding value as that user's password.
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

Dependencies:

- :ref:`supervisor.pip`
- :ref:`project.dirs`
- :ref:`project.venv`

.. _project.worker.default:

project.worker.default
~~~~~~~~~~~~~~~~~~~~~~

Arrange for a ``celery worker`` service to run for the project via supervisor.

Dependencies:

- :ref:`supervisor.pip`
- :ref:`project.dirs`
- :ref:`project.venv`
- :ref:`postfix`

.. _python:

python
~~~~~~

Installs the version of python specified in Pillar as
``python_version``, along with a variety of dev libraries like ``libjpeg8-dev`` that
are needed to install various Python packages like Pillow, as well
as setuptools, pip, and virtualenv.  Also makes a few symlinks that
help with building Pillow on 64bit systems.

Also installs ``ghostscript`` ?!?!?!?!!

.. _rabbitmq:

rabbitmq
~~~~~~~~

Install rabbitmq and make it run.

Delete the default ``guest`` rabbitmq user.

.. _salt.master:

salt.master
~~~~~~~~~~~

Opens ports 4505 and 4506.

Dependencies:

- :ref:`ufw`

.. _solr:

solr
~~~~

Installs ``openjdk-7-jre-headless``.

.. _solr.project:

solr.project
~~~~~~~~~~~~

Installs Solr and copies the default stopwords file into its
configuration.

Does not appear to arrange to run it.

Dependencies:

- :ref:`solr`

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

.. _sshd.github:

sshd.github
~~~~~~~~~~~

Add ``github.com`` to the system known hosts file.

.. _statsd:

statsd
~~~~~~

Install statsd and provide basic default configuration, arranging
for it to run on startup.

Dependencies:

- :ref:`nodejs`
- :ref:`version-control`

.. _syslog:

syslog
~~~~~~

Arrange to install rsyslog v8.5 or later.

Configure it to load the `imfile` module so that other states
can add rsyslog config files to tell rsyslog to monitor plain
text log files.

.. _sudo:

sudo
~~~~

Arrange for sudo service to run.

Update the ``sudoers`` config file to let users in group ``admin``
do anything without a password.

.. _supervisor:

supervisor
~~~~~~~~~~

.. deprecated:: forever
  Use ``supervisor.pip`` instead.

Install and run supervisor using its Debian/Ubuntu package.

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

.. _vagrant.user:

vagrant.user
~~~~~~~~~~~~

Add the ``vagrant`` user to the ``admin`` and ``login`` groups so that
with our updated configuration for ``ssh`` and ``sudo``, the vagrant user
can still login and do things as root.

Dependencies:

- :ref:`users.groups`

.. _version-control:

version-control
~~~~~~~~~~~~~~~

Install git, mercurial, and subversion.
