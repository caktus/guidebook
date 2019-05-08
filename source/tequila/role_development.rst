.. _tequila-role-development:

Role Development
================

To start with, clone the repo to your local machine.  In this example,
we'll use the tequila-common role ::

    $ git clone git@github.com:caktus/tequila-common.git
    $ cd tequila-common/

Then, within some existing project, uninstall the pinned version of
the role and replace it with a symlink to the checkout.  The following
assumes that you have Ansible configured to install roles into the
deployment/roles/ directory within your Django project's tree ::

    $ cd my-django-project/
    $ workon project
    (project)$ ansible-galaxy remove tequila-common
    (project)$ cd deployment/roles/
    (project)$ ln -s /path/to/tequila-common

Now when you make changes to the tasks or files in your checkout of
the role, those changes will be immediately available when you
do a deployment for this project.

When finished trying out your changes, be sure to remove the symlink
and reinstall the pinned version ::

    (project)$ rm deployment/roles/tequila-common
    (project)$ ansible-galaxy install -r deployment/requirements.yml
