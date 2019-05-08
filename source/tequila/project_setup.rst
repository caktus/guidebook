.. _tequila-project-setup:

Adding Tequila to a Django Project
==================================

#. Add some basic directory structure.

   By convention, our Tequila project configuration is expected to be
   in the deployment/ directory of the repo.  Add this directory, then
   underneath it add environments/, playbooks/, and keys/
   directories. ::

       sample-project/
       └── deployment
           ├── environments
           ├── keys
           └── playbooks

#. At the root of the repo, add an ansible.cfg file.  Fill it with at
   least this ::

       [defaults]
       roles_path = deployment/roles/
       vault_password_file = .vault_pass

   This will make sure that the Ansible / Tequila roles get installed
   in the right place for your project, and that the secrets files can
   get decrypted and read without having to pass an extra flag to the
   ansible commands each time.  Commit this file.

#. At the root of the repo, create a file called .vault_pass, and fill
   it with a generated secret, such as from the output of pwgen.  **DO
   NOT** commit this to the repo, instead share the secret to the rest
   of your team via some more secure means, such as LastPass.  Add
   this filename as an entry in the project's .gitignore file so that
   no one is tempted to commit it to the repo in the future.

#. **Optional:** Create a package.json file in the root of the repo,
   if one does not already exist.  A bare-bones file can look like
   this ::

       {
         "name": "sample_project",
         "dependencies": {
         }
       }

#. In the deployment/ directory, create a requirements.yml file.  This
   file will specify which Tequila or other Ansible roles this project
   will use for deployments.  For a typical project, this should
   probably consist of something like this ::

       ---
       - src: https://github.com/caktus/tequila-common
         version: v0.8.1
         name: tequila-common

       - src: https://github.com/caktus/tequila-postgresql
         version: v0.8.0
         name: tequila-postgresql

       - src: https://github.com/caktus/tequila-nginx
         version: v0.8.5
         name: tequila-nginx

       - src: https://github.com/caktus/tequila-django
         version: v0.9.8
         name: tequila-django

       - src: geerlingguy.nodejs
         version: 4.1.2

       - src: https://github.com/caktus/tequila-nodejs
         version: v0.8.0
         name: tequila-nodejs

       - src: https://github.com/caktus/tequila-rabbitmq
         version: v0.8.1
         name: tequila-rabbitmq

   Check to see what the most recent version is for each.

   For needs that are not fulfilled by the (currently) six Tequila
   roles, feel free to find an appropriate 3rd-party role on Ansible
   Galaxy rather than trying to roll your own.  We are currently
   making use of several roles created by `geerlingguy
   <https://galaxy.ansible.com/geerlingguy/>`_, one of the Ansible
   core developers, on our projects.

#. If you were to install the roles from the requirements file now, a
   deployment/roles/ directory would automatically be created and all
   of your specified roles would be downloaded into it.  We do not
   want to check any of those into the repo, so add
   ``/deployment/roles/`` to the project's .gitignore file.  While you
   are at it, also add ``*.retry`` to the .gitignore file, to ignore
   the files left behind when a deployment fails.

   Now that you've added ``/deployment/roles/`` and ``*.retry`` to the
   .gitignore file, you can install each of the entries in
   ``deployment/requirements.yml`` using::

       ansible-galaxy install -r deployment/requirements.yml

#. In deployment/playbooks/, copy over the selection of playbook files
   from the playbooks/ directory of this repo.  Currently this should
   be, at a minimum, bootstrap_python.yml (a small playbook used to
   deal with later versions of Ubuntu and Debian lacking Python 2 by
   default), common.yml (a playbook for executing the tequila-common
   Ansible role), db.yml (tequila-postgresql), queue.yml
   (tequila-rabbitmq), web.yml (tequila-nginx, tequila-django, and
   tequila-nodejs), worker.yml (tequila-django used for Celery), and
   site.yml (a catch-all playbook that uses the include directive to
   pull in at least the common, db, web, worker, and queue playbooks).
   Other playbooks should be created as needed to fill other
   project-specific needs. For instance, bootstrap_db.yml may be used
   for setting up an AWS RDS database, and search.yml may be used for
   setting up Elasticsearch.

   Make sure to sanity check the contents of each playbook for
   applicability to the project.

#. Within the deployment/playbooks/ directory, create a
   group_vars/all/ subdirectory.  Create empty devs.yml and
   project.yml files in this subdirectory.  The devs.yml file will
   hold the list of developers that will have access to the servers
   and their ssh keys.  The project.yml file will hold the
   configuration variables for the project as a whole.

#. Under deployment/environments/, create a directory for each
   environment that the project supports.  This should probably
   include at least production/, staging/, and vagrant/.  For now, add
   an empty inventory file to each of these environment
   subdirectories. ::

       deployment/environments/
       ├── production
       │   └── inventory
       ├── staging
       │   └── inventory
       └── vagrant
           └── inventory

   These inventory files will hold the address of each server for that
   environment and what role groups they are part of.

#. In each deployment/environments/<envname>/ directory, create
   group_vars/all/ subdirectories.  Within each
   deployment/environments/<envname>/group_vars/all/ directory, add
   empty secrets.yml and vars.yml files. ::

       deployment/environments/
       ├── production
       │   ├── group_vars
       │   │   └── all
       │   │       ├── secrets.yml
       │   │       └── vars.yml
       │   └── inventory
       ├── staging
       │   ├── group_vars
       │   │   └── all
       │   │       ├── secrets.yml
       │   │       └── vars.yml
       │   └── inventory
       └── vagrant
           ├── group_vars
           │   └── all
           │       ├── secrets.yml
           │       └── vars.yml
           └── inventory

   The secrets.yml files will hold the secrets for that environment,
   and will be encrypted by ansible-vault before being committed to
   the repo.  The vars.yml files will hold the environment-specific
   configuration variables.

#. **Optional:** Update or create the Makefile, if needed, using the
   copy from `caktus/django-project-template
   <https://github.com/caktus/django-project-template/blob/master/Makefile>`_
   as a guide.  There is probably not too much that needs to change
   here, other than changing references from conf/ to deployment/.

   It is possible to get by without this Makefile, but it is still
   strongly recommended to have some means of generating
   per-environment ssh keys to use to grant permission for your
   servers to check out a copy of the repo from your source control
   service (whether that is github.com or some other one).

#. Create public deployment ssh keys using the Makefile (e.g. ``make
   deployment/keys/staging.pub.ssh``) or some other means, or move
   over the existing ones (e.g. ``mv -i conf/keys/*.pub.ssh
   deployment/keys/``).  If you do create new ones, add them to the
   github repo's "Deploy keys" setting.

#. Fill in the developer usernames and ssh keys into
   deployment/playbooks/group_vars/all/devs.yml.  Tequila expects the
   ``users`` variable to be a list of dicts, each dict having the keys
   ``name`` and ``public_keys``, the latter of which is itself a list
   of ssh keys.  This should result in a file that looks like this ::

       ---
       users:
         - name: user1
           public_keys:
             - "ssh-rsa AAAA..."

         - name: user2
           public_keys:
             - "ssh-rsa AAAA..."

   (**Caktus-specific:** The format of this file is slightly different
   than the equivalent file for `Margarita
   <https://github.com/caktus/margarita>`_, usually found in
   conf/pillar/devs.sls.)

   For conversions of existing projects, now is a good time to prune
   no-longer-active developers and add new devs that might work on the
   project.

#. Fill in the global project variables in
   deployment/playbooks/group_vars/all/project.yml.  Typically it will
   look something like this ::

       ---
       project_name: sample_project
       python_version: 3.5
       pg_version: 9.5
       gunicorn_version: 19.7.1

       repo:
         url: "{{ repo_url|default('git@github.com:caktus/sample-project.git') }}"
         branch: "{{ repo_branch|default('master') }}"

       requirements_file: "{{ source_dir }}/requirements/production.txt"

       app_minions: "{{ groups['web'] | union(groups['worker']) }}"

       nodejs_version: "6.x"
       nodejs_install_npm_user: "{{ project_name }}"
       nodejs_package_json_path: "{{ source_dir }}"

       github_deploy_key: "{{ SECRET_GITHUB_DEPLOY_KEY|default('') }}"
       # db_host: per environment
       db_name: 'sample_project_{{ env_name }}'
       db_user: 'sample_project'
       db_password: "{{ SECRET_DB_PASSWORD }}"
       secret_key: "{{ SECRET_KEY }}"

   Note that the convention that we have settled upon is for secret
   variables to be defined (within encrypted secrets.yml files) with
   names in all-caps and prefixed with ``SECRET_``, and then the
   actual expected variables to be explicitly set to the value of
   those secret values.  This allows the variable names to be
   grep-able, which they wouldn't be if they were set directly in the
   encrypted secrets.yml files.

   A note about the ``project_name``: Though it is not obvious here, this
   variable must be a valid python module, because it gets imported during
   the deploy. For example, setting ``project_name`` to ``sample-project``
   will throw an error during the deploy.

   While tequila-postgresql and -django do define a default database
   name, it turns out that it is a good idea to have this variable
   explicitly defined so that it may also be used for other playbooks,
   e.g. bootstrap_db.yml.

#. Fill in the non-secret variables for each environment under
   deployment/environments/<envname>/group_vars/all/vars.yml.  A
   simple vars.yml file might look like this ::

       ---
       env_name: staging
       domain: sp-staging.caktus-built.com
       repo_branch: develop
       cert_source: letsencrypt
       force_ssl: true
       cloud_staticfiles: false
       source_is_local: false
       gunicorn_num_workers: 2
       use_newrelic: true
       new_relic_license_key: "{{ SECRET_NEW_RELIC_LICENSE_KEY }}"

       extra_env:
         NEW_RELIC_LICENSE_KEY: "{{ new_relic_license_key }}"
         NEW_RELIC_APP_NAME: "'sample_project staging'"

   Refer to the README.rst of each of the Tequila roles for the
   meaning and allowed values of each variable.

   The ``extra_env`` dictionary is intended to forward on any
   variables in it into the .env file that gets deployed, so use this
   for any env vars that you need that are not already included in the
   templates/envfile.j2 file within the version of tequila-django that
   you are using.

   If you are intending to use a Let's Encrypt SSL certificate in a
   fresh environment, first you have to deploy to the environment with
   SSL turned off, so that the 'certonly' mode of certbot-auto has a
   webserver that it can provide its special file on.  Deploy first
   with ``force_ssl: false`` and ``cert_source: none``, then after
   that deployment completes and you have verified that the site is
   accessible, deploy again with ``force_ssl: false`` and
   ``cert_source: letsencrypt``.  This should result in a certificate
   being successfully obtained.  After this, ``force_ssl`` may be set
   to ``true``, to match our usual practice.

#. Fill in the secret variables for each environment under
   deployment/environments/<envname>/group_vars/all/secrets.yml.  This
   will include things like the Django secret key, the database
   password, and the private half of the Github deploy key that you
   created or copied over a few steps back.  Examine the secrets files
   of other Tequila-based projects for examples.

   Make sure that every secret variable has a corresponding clear-text
   use in either project.yml or the environment-specific vars.yml, as
   noted in the non-secret variables step above.

   After this file is filled in, encrypt it using ``ansible-vault
   encrypt
   deployment/environments/<envname>/group_vars/all/secrets.yml``.
   This will make use of the secret that you generated earlier and put
   into .vault_pass to encrypt the file.  **NEVER** commit these files
   in an unencrypted state.

   In order to make further edits, you may use the command
   ``ansible-vault decrypt
   deployment/environments/<envname>/group_vars/all/secrets.yml`` to
   turn it back into plaintext.

#. **Caktus-specific:** Do any still-needed steps suggested by the
   `Upgrading Margarita
   <http://caktus.github.io/developer-documentation/margarita/upgrading.html#single-deploy-settings>`_
   developer documentation, beginning at the Single Deploy Settings
   section.

#. Fill in the server information in each of the environments'
   inventory files.  An inventory file for a simple, one-server
   project may look like this ::

       staging ansible_host=42.42.42.42

       [web]
       staging

       [db]
       staging

       [queue]
       staging

       [worker]
       staging

   Multiple servers may be defined above the group sections, using
   different names for each.  The value of ``ansible_host`` may be an
   IP address, or a fully qualified domain name
   (e.g. ec2-42-42-42-42.us-east-2.compute.amazonaws.com).  Additional
   variables may be defined here, if necessary.

   For the server groups, fill in or leave out servers depending upon
   the role that they are intended to serve.  Servers in the ``[web]``
   section are intended to run nginx and Django, those in ``[db]`` are
   intended to have a PostgreSQL cluster set up and running, those in
   ``[queue]`` will provide the RabbitMQ queue for any Celery tasks,
   and those in ``[worker]`` will be Celery workers.

   Note that RDS database instances, if they are used by a project, do
   not go in the ``[db]`` section.  This section is reserved for
   databases that are manually set up and managed.  Currently the
   bootstrap_db.yml playbook, and in the future the tequila-django
   role, will be sufficient for initializing an RDS database.

   **TODO:** Provide a naming scheme that is picked up by a task in
   tequila-common to set each instance's hostname.

#. **Caktus-specific:** Look through the project's conf/salt/ tree,
   looking for any customization away from stock Margarita.  Any such
   will probably need to be dealt with using new playbooks or added
   tasks to the existing deployment playbooks.

#. **Caktus-specific:** Update the fabfile.py, removing all of the
   Salt-specific commands, and updating the others to use calls to
   ansible-playbook.  Take a look at the fabfile.py from other
   projects using Tequila as a guide.

#. **Caktus-specific:** Remove install_salt.sh.

#. Create or update the Vagrantfile.  The best practice as currently
   understood for Tequila-based projects is to add call-outs to the
   bootstrap_python.yml and common.yml playbooks to the provisioning,
   like so ::

       config.vm.provision "ansible" do |ansible|
         config.ssh.username = "vagrant"
         ansible.inventory_path = "deployment/environments/vagrant/inventory"
         ansible.limit = "all"
         ansible.playbook = "deployment/playbooks/bootstrap_python.yml"
       end

       config.vm.provision "ansible" do |ansible|
         config.ssh.username = "vagrant"
         ansible.inventory_path = "deployment/environments/vagrant/inventory"
         ansible.limit = "all"
         ansible.playbook = "deployment/playbooks/common.yml"
       end

   Adding common.yml to the provisioning like this allows the
   developers to be able to authenticate without the need to specify
   the often-fragile Vagrant ssh key for deployments.

#. **Caktus-specific:** Update the project README.rst file to remove
   Salt-specific information, add new Tequila info (which may be
   distilled from other projects using Tequila), and make any changes
   relevant to updates in process (e.g. use of .env files).

#. **Caktus-specific:** Update any documentation in the docs/
   directory to remove Salt-based instructions and add in
   Tequila-based ones.

#. When standing up new environments, remember that you need to make
   sure that Python 2 is set up on the new servers in order for most
   Ansible tasks to be successfully performed.  Setting this up can be
   done using ``fab <envname> bootstrap_python`` (if you are using a
   Caktus-style fabfile.py and it has such a command) or directly
   using the ansible command ``ansible-playbook -i
   deployment/environments/<envname>/inventory
   deployment/playbooks/bootstrap_python.yml``.

   Note: in case you are running this command before you have set up users,
   you will get a "Permission denied" error (since your user does not yet
   exist). Instead, you must run the command as the root user:
   ``ansible-playbook -i deployment/environments/<envname>/inventory -u root
   deployment/playbooks/bootstrap_python.yml``
   Some environments may have different requirements. For example, an Ubuntu
   server on AWS requires you to run the command as ``ubuntu``, and to pass
   the private key:
   ``ansible-playbook -i deployment/environments/<envname>/inventory -u ubuntu
   --private-key=<path to private key> deployment/playbooks/bootstrap_python.yml``

#. If you created new ssh deployment keys, revoke the old ones on
   github.com after the cutover.
