.. _upgrading:

Upgrading Margarita
===================

Before attempting to upgrade your project's Margarita version, please read `the overview document
about Margarita upgrades
<https://github.com/caktus/django-project-template/blob/master/docs/updates.rst>`_ first, to get a
high level view of the changes required.

This document is going to outline the steps involved in upgrading a project which is using the
master branch of Margarita. We will be upgrading it to Margarita 1.4.0. Following this guide should
allow you to upgrade projects in a similar scenario. Projects which are already using a pinned
version of Margarita should be able to upgrade by following the `Margarita release notes
<https://github.com/caktus/margarita/blob/develop/CHANGES.rst>`_

This guide assumes that all services are running on one server (with a pretend IP address of
1.2.3.4). If you have a multiple server setup, then anytime a fabric command has an ``-H`` flag,
you'll have to repeat that command once for each IP address in your fleet.


Prepare Repository
------------------

.. WARNING::
   The new project template does not 'reconcile' secrets because it assumes that you have
   committed the encrypted versions to the repo, so syncing back-and-forth is not necessary. We
   haven't yet done that step for our project, so we need to be very careful about our secrets.
   Make sure to sync them (by doing a deploy or running ``fab get_secrets``) before going any
   further.


1. Get useful files from the new project template. Clone the `Django Project Template
   <https://github.com/caktus/django-project-template>`_ repo  into a directory adjacent to ours, so
   we can easily copy files we need:

   .. code-block:: bash

      ~/dev$ git clone git@github.com:caktus/django-project-template.git
      ~/dev$ ls
      django-project-template myproject
      ~/dev$ cd myproject
      ~/dev/myproject$


#. Copy some important files and directory to our project:

   .. code-block:: bash

      ~/dev/myproject$ mv fabfile.py fabfile.py.old
      ~/dev/myproject$ cp ../django-project-template/fabfile.py .
      ~/dev/myproject$ cp ../django-project-template/Vagrantfile .
      ~/dev/myproject$ cp ../django-project-template/install_salt.sh .
      ~/dev/myproject$ cp ../django-project-template/conf/master.tmpl conf/
      ~/dev/myproject$ rm conf/master.conf
      ~/dev/myproject$ cp ../django-project-template/conf/gpg.tmpl conf/

#. Edit fabfile.py:

   1. Make sure ``SALT_VERSION`` is ``2015.5.8``
   2. Change ``env.master`` in both the ``staging()`` and ``production()`` functions to be
      correct (get the value from fabfile.py.old)


Upgrade Margarita
-----------------

#. Add to ``conf/pillar/project.sls``:

   .. code-block:: yaml

      margarita_version: 1.5.0
      less_version: 1.5.1   # or whatever you're currently using
      postgres_version: 9.1 # or whatever you're currently using

#. Move the old states out of the way (don't leave them in the conf directory), and copy in the
   minimal new list:

   .. code-block:: bash

      ~/dev/myproject$ mv conf/salt salt.old
      ~/dev/myproject$ cp -r ../django-project-template/conf/salt conf/


Single Deploy settings
----------------------

Our current deployment expects all Django settings to be in a single module named ``deploy.py``.
We need to merge the ``staging.py`` and ``production.py`` files into one called ``deploy.py``.
The easiest way is to create a new file called ``deploy.py`` with this content:

.. code-block:: python

   import os
   ENVIRONMENT = os.environ['ENVIRONMENT']
   if ENVIRONMENT == 'staging':
       from .staging import *
   elif ENVIRONMENT == 'production':
       from .production import *
   else:
       from .local import *

That should be refactored ASAP to get rid of the staging and production files.

Dotenv
------

#. Add ``myproject/load_env.py`` (same dir as root ``urls.py``):

   .. code-block:: python

      from os.path import dirname, join
      import dotenv


      def load_env():
          "Get the path to the .env file and load it."
          project_dir = dirname(dirname(__file__))
          dotenv.read_dotenv(join(project_dir, '.env'))

#. Modify ``myproject/celery.py``:

   .. code-block:: diff

      Modified   myproject/celery.py
      diff --git a/myproject/celery.py b/myproject/celery.py
      index d9a4e87..4f5a199 100644
      --- a/myproject/celery.py
      +++ b/myproject/celery.py
      @@ -11,2 +11,5 @@ from celery import Celery

      +from . import load_env
      +load_env.load_env()
      +

#. Modify ``myproject/wsgi.py``:

   .. code-block:: diff

      Modified   myproject/wsgi.py
      diff --git a/myproject/wsgi.py b/myproject/wsgi.py
      index 69e0323..28cb28d 100644
      --- a/myproject/wsgi.py
      +++ b/myproject/wsgi.py
      @@ -16,3 +16,5 @@ framework.
       import os
      +from . import load_env

      +load_env.load_env()

#. Modify ``manage.py``:

   .. code-block:: diff

      Modified   manage.py
      diff --git a/manage.py b/manage.py
      index cb48c9e..8bc2fce 100644
      --- a/manage.py
      +++ b/manage.py
      @@ -4,2 +4,5 @@ import sys

      +import dotenv
      +dotenv.read_dotenv()
      +
       if __name__ == "__main__":

#. Modify ``requirements/base.txt``:

   .. code-block:: diff

      Modified   requirements/base.txt
      diff --git a/requirements/base.txt b/requirements/base.txt
      index 2bb6ff2..ca74917 100644
      --- a/requirements/base.txt
      +++ b/requirements/base.txt
      +
      +django-dotenv==1.3.0

#. Modify ``README.rst`` (and follow those instructions for your local setup):

   .. code-block:: diff

      Modified   README.rst
      diff --git a/README.rst b/README.rst
      index c45b564..8c456be 100644
      --- a/README.rst
      +++ b/README.rst
      @@ -27,7 +27,9 @@ necessary requirements::

      -Then create a local settings file and set your ``DJANGO_SETTINGS_MODULE`` to use it::
      +Next, we'll set up our local environment variables. We use `django-dotenv
      +<https://github.com/jpadilla/django-dotenv>`_ to help with this. It reads environment variables
      +located in a file name ``.env`` in the top level directory of the project. The only variable we need
      +to start is ``DJANGO_SETTINGS_MODULE``::

      -    cp myproject/settings/local.example.py myproject/settings/local_dev.py
      -    echo "export DJANGO_SETTINGS_MODULE=myproject.settings.local_dev" >> $VIRTUAL_ENV/bin/postactivate
      -    echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate
      +    (myproject)$ cp myproject/settings/local.example.py myproject/settings/local.py
      +    (myproject)$ echo "DJANGO_SETTINGS_MODULE=myproject.settings.local" > .env


Update ALLOWED_HOSTS
--------------------

Find the ``ALLOWED_HOSTS`` setting (probably in ``staging.py``) and change it to use ``DOMAIN``:

.. code-block:: diff

   Modified   myproject/settings/staging.py
   diff --git a/myproject/settings/staging.py b/myproject/settings/staging.py
   index db7b3b4..be4024d 100644
   --- a/myproject/settings/staging.py
   +++ b/myproject/settings/staging.py
   @@ -34,3 +34,3 @@ SESSION_COOKIE_HTTPONLY = True

   -ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(';')
   +ALLOWED_HOSTS = [os.environ['DOMAIN']]

Frontend Improvements
---------------------

Prepare for Calvin's frontend improvements. Add a *dummy* ``package.json`` which can be updated
later. Until it is updated, the frontend improvements won't take effect:

.. code-block:: json

   {
     "name": "",
     "version": "0.0.0",
     "description": "",
     "main": "",
     "engines" : {
       "node" : ">=4.2 <4.3"
     },
     "scripts": {
       "build": "true"
     },
     "author": "",
     "license": "",
     "dependencies": {},
     "devDependencies": {}
   }


Miscellaneous work
------------------

Technically, you can skip the steps in this section and come back to them later. Even without them,
you should be able to get a server upgraded, but they **will** have to be done at some point.

1. Port any useful functions in ``fabfile.py.old`` to the new fabfile, then remove the old one.

#. Get a copy of the ``Makefile`` from the project template, porting any functions in your existing
   one to the new one, if needed.

#. Review everything in ``salt.old`` to see which pieces are specific to your project and need to
   be added back into salt. If any of it is generally useful (i.e. setting up a service that
   might be used on another project), then consider adding a PR to margarita so this config can
   be completely removed from your project.

   This part is difficult to generalize... Sorry. You kinda have to look in each state file and
   make sure that service is properly accounted for in the new Margarita system.

#. Look at the following files in django-project-template to see if your project could benefit
   from any changes:

   * .coveragerc
   * .gitignore
   * README.rst
   * setup.cfg
   * .travis.yml (look at project.travis.yml)

Vagrant Smoke Test
------------------

Now, we're going to create a fresh Vagrant VM just to make sure that our current repository deploys
correctly.

#. Edit ``conf/pillar/local/env.sls`` to look like this:

   .. code-block:: yaml

      environment: local
      domain: margarita.example.com

#. Edit ``conf/pillar/local/secrets.sls`` to look like this:

   .. code-block:: yaml

      secrets:
        DB_PASSWORD: "dbPassword"
        BROKER_PASSWORD: "brokerPassword"

#. Add the following line to your laptop's ``/etc/hosts`` file::

     33.33.33.10 margarita.example.com

#. Make sure we're starting from a fresh VM:

   .. code-block:: bash

      ~/dev/myproject$ vagrant destroy
      ~/dev/myproject$ vagrant up

#. Deploy!

   .. code-block:: bash

      ~/dev/myproject$ fab vagrant setup_master
      ~/dev/myproject$ fab -H 127.0.0.1:2222 vagrant setup_minion setup_minion:salt-master,web,worker,balancer,db-master,queue,cache
      ~/dev/myproject$ fab vagrant deploy

#. If that works, you should see your site at https://margarita.example.com.


.. _update-repo:

Update Repo Code
----------------

.. NOTE:: We will upgrade Salt on the staging machine. Once you have completed the upgrade process
          and verified that it is working perfectly, you'll need to repeat the process for `updating
          production`_. When you get to that point, our instructions will point you back here to
          repeat the process for production. Just follow these instructions, replacing *staging*
          with *production*, and *develop* with *master*.

Once you have gotten the smoke test to work successfully, we'll need to get all of these changes
into a branch that salt will be able to checkout on the staging server.

#. Commit your changes locally.
#. Push your changes to a feature branch (*your-feature-branch*) on Github.
#. Update ``repo.branch`` in ``conf/pillar/staging/env.sls`` from *develop* to
   *your-feature-branch*. Remember to change this back to its original value when this entire
   process is successful. The default is *develop* for staging and *master* for production.


.. _upgrade-salt:

Upgrade Salt
------------

1. Fetch a copy of ``/etc/salt/minion`` from the server. We'll need which roles are currently being
   used, so we can setup the same roles when we call ``setup_minion`` in step 5.

   .. code-block:: bash

      ~/dev/myproject$ scp 1.2.3.4:/etc/salt/minion old-minion.conf

#. Uninstall salt. We're using the ``--force-yes`` parameter because salt packages are *held* on
   some of our servers, so this is needed to allow uninstallation. **Make sure you are using the new
   fabfile!**

   .. code-block:: bash

      ~/dev/myproject$ fab -H 1.2.3.4 staging -- sudo apt-get remove salt-master salt-minion salt-common -y --force-yes

#. If you are on Ubuntu 12.04, run this command to enable backports, needed for python-gnupg:

   .. code-block:: bash

      ~/dev/myproject$ fab -H 1.2.3.4 staging -- sudo sed -i '/precise-backports/s/^#//g' /etc/apt/sources.list

#. Set up the salt master.

   .. code-block:: bash

      ~/dev/myproject$ fab staging setup_master

#. Set up the salt minion. Get the list of roles from the ``old-minion.conf`` you saved in step 1.
   The example below shows all possible roles being assigned to this minion.

   .. code-block:: bash

      ~/dev/myproject$ fab -H 1.2.3.4 staging setup_minion:salt-master,web,worker,balancer,db-master,queue,cache

   .. NOTE:: Make sure ``salt-master`` is in there. It seems to be absent in some projects, but
             if you're running everything on a single box it should be there.


Sync
----

#. Sync these states over to the server (do this separately from the actual deploy so that
   failures can be caught before actually trying to deploy)

   .. code-block:: bash

      ~/dev/myproject$ fab staging sync


Deploy!!!
---------

.. code-block:: bash

   ~/dev/myproject$ fab staging deploy

And of course that worked! If not, let us know so we can help.


.. _encrypt-secrets:

Encrypt Secrets
---------------

This must be done because the new fabfile has removed the *secrets-syncing* logic, so unsuspecting
developers **will likely** stomp on each others secrets. Encrypting cannot be done until
``setup_master`` has run successfully. We'll do staging now, but we can't do production until we've
run ``setup_master`` on production.

1. Add this declaration to the top of ``conf/pillar/staging/env.sls``::

     #!yaml|gpg

#. Copy everything from ``conf/pillar/staging/secrets.sls`` to ``conf/pillar/staging/env.sls``.

#. For each key that you've just added to the file, encrypt the value and replace the value in
   ``env.sls`` with the encrypted value. (See the `docs
   <https://github.com/caktus/django-project-template/blob/master/docs/provisioning.rst#managing-secrets>`_
   for more details):

   .. code-block:: bash

      ~/dev/myproject$ fab staging encrypt:DB_PASSWORD='superSecretPassword'
      "DB_PASSWORD": |-
        -----BEGIN PGP MESSAGE-----
        Version: GnuPG v1

        hIwDi3G8b0sD8fkBA/4kMuhn2YmdKhyy99Xi3Nn6XOUmY/oikyU1AF68ynHfywNd
        zcu8xcA0iHhj/eK7dDvC9eE94xUNNoPkddU+J6ulzhEIzQFWndD5YCO1WyHWLYbq
        N48BPaiUHWoiWFKA4aApPJHPfiV6JJUxiwHadhoAseOQw94ce75fUqbe4RiXrNJS
        ATFNQz0dtCF8H0VhYBUYHvF7yHuhZVeOqgTT93B0tDGCy9rq47Dq3PnjityrFuAL
        TLNW7zsjjEuA1P6HZ8xwRqYwSJ4MF8tkXDUX3Q++cGlW6w==
        =w3nx
        -----END PGP MESSAGE-----

   Replace the key and value in ``env.sls`` with the output of that command.

#. For the github deploy key (if present) or any other multi-line values, it's better to copy the
   unencrypted key data to its own file, (named ``github_key.priv`` in this example), remove any
   indentation, and then run:

   .. code-block:: bash

      ~/dev/myproject$ fab staging encrypt:github_key.priv

   The encrypted version will then be in ``github_key.priv.asc``. Copy the content from that file
   into ``env.sls``.

#. Move the ``secrets.sls`` file out of the way:

   .. code-block:: bash

      ~/dev/myproject$ mv conf/pillar/staging/secrets.sls staging-secrets.sls

#. Rename ``env.sls``:

   .. code-block:: bash

      ~/dev/myproject$ mv conf/pillar/staging/env.sls conf/pillar/staging.sls
      ~/dev/myproject$ rmdir conf/pillar/staging

#. Update the ``conf/pillar/top.sls`` file:

   .. code-block:: diff

      Modified   conf/pillar/top.sls
      diff --git a/conf/pillar/top.sls b/conf/pillar/top.sls
      index 720b942..0db9e8a 100644
      --- a/conf/pillar/top.sls
      +++ b/conf/pillar/top.sls
      @@ -10,4 +10,3 @@ base:
           - match: grain
      -    - staging.env
      -    - staging.secrets
      +    - staging
         'environment:production':

#. Commit, push, and redeploy:

   .. code-block:: bash

      ~/dev/myproject$ fab staging deploy

Updating Production
-------------------

If staging updates successfully, it's time to take care of the production machine. Follow the steps
above, starting from the :ref:`Update Repo Code <update-repo>` pathway above, but on the production
machine.

If you get this far and everything is working then it's time to celebrate!! Make sure that the
*develop* and *master* branches are properly updated with the changes in *your-feature-branch* and
that ``repo.branch`` is set to the correct value in ``conf/pillar/<environment>.sls``.

Troubleshooting
---------------

Here are some issues that may or may not come up during your upgrade. As we find new issues, we
should update the docs above (if they are general), or add them here, if they aren't general or
we're not sure.

* ``newrelic_license_key`` must be capitalized. Some projects have a secret for
  ``newrelic_license_key``, but the current margarita uses ``NEW_RELIC_LICENSE_KEY``

* NewRelic settings may need adjusting, which you can do via environment variables (see
  other documentation in this repo for details).

* If you get timeout errors during the first deploy, it may be because of a few different issues.

  * Low CPU/RAM servers might need the salt timeouts extended. Add ``timeout: 600`` to
    ``/etc/salt/master`` and ``/etc/salt/minion`` (or edit the value if already present) and then
    restart both the ``salt-master`` and ``salt-minion``. Wait a **full minute** or so before
    starting any salt command. My salt-minions took a loooong time to start on a low-powered box.

  * There might be a chicken/egg problem with the firewall. Do a grep for ``UFW BLOCK`` in
    ``/var/log/syslog``::

      Jan 13 21:19:48 ip-<deleted> kernel: [78350448.038946] [UFW BLOCK] IN=eth0 OUT= MAC=<deleted> SRC=<deleted> DST=<deleted> LEN=60 TOS=0x00 PREC=0x00 TTL=45 ID=33808 DF PROTO=TCP SPT=53084 DPT=4506 WINDOW=14600 RES=0x00 SYN URGP=0

    That says port 4506 (DPT) is being blocked by the firewall. If so, run::

      # ufw allow salt

  If salt is installed, the command above will open up the ports that salt needs. Our deploy does
  that too, but if the firewall is already running, then our salt state can't run. I'm still
  confused how this problem happened on a server which had already been running salt successfully,
  but ¯\\_(ツ)_/¯.

* *VAGRANT NOTE*: Make sure to undo the ``Vagrantfile`` setting which syncs the conf folder to
  ``/srv`` on the VM, because the project no longer expects that folder to be synced, so will run
  into problems trying to change permissions on the files there.

  Change this::

    config.vm.synced_folder "conf/", "/srv/"

  to::

    config.vm.synced_folder "conf/", "/srv/", disabled: true

  and then restart the VM. If you are using the new ``Vagrantfile``, you shouldn't need to do that.

* *VAGRANT NOTE:* Remove the ``source`` and ``public`` symlinks as we rsync now rather than symlink.

  .. code-block:: bash

     ~/dev/myproject$ fab -H 127.0.0.1:2222 vagrant -- sudo rm /var/www/myproject/source
     ~/dev/myproject$ fab -H 127.0.0.1:2222 vagrant -- sudo rm /var/www/myproject/public

* If you see an error like the following, it means that your local ``conf`` directory has contents
  that it shouldn't. Remove the file/directory in question locally and then rerun the sync command.

  .. code-block:: bash

     [54.234.112.22] out: mv: cannot move `/tmp/salt/local' to `/srv/local': Directory not empty
