.. _tequila:

Tequila
=======

Tequila is our Ansible-based deploy framework.

Tequila is a collection of `Ansible
<http://www.ansible.com/home>`_ roles for deployments of `Django
<https://docs.djangoproject.com/>`_ projects, working together with
the `Caktus Django project template
<https://github.com/caktus/django-project-template>`_,
playbooks from `<https://github.com/caktus/tequila>`_,
and the `tequila-fab <https://github.com/caktus/tequila-fab>`_
Python package.

Setting Up Tequila
------------------

For projects that have not used Tequila before, check out the
:ref:`tequila-project-setup`
documentation. This document also provides helpful hints for projects switching
from :ref:`margarita`.

Roles
-----

Most roles provide fairly comprehensive documentation in their
README files.

`tequila-common <https://github.com/caktus/tequila-common>`_
    Install common system packages, set up server users and keys, add
    some basic security configuration, and create the standard project
    directory structure.

`tequila-nginx <https://github.com/caktus/tequila-nginx>`_
    Install and configure `nginx <https://nginx.org/en/docs/>`_ as a
    forwarding proxy for a Django project.

`tequila-django <https://github.com/caktus/tequila-django>`_
    Set up a Django project to run under `gunicorn
    <http://docs.gunicorn.org/en/stable/>`_ and/or `Celery
    <http://docs.celeryproject.org/en/latest/>`_.

`tequila-nodejs <https://github.com/caktus/tequila-nodejs>`_
    A thin wrapper around `geerlingguy/nodejs
    <https://github.com/geerlingguy/ansible-role-nodejs>`_,
    tequila-nodejs installs nodejs and npm, installs your project
    dependencies, and executes your front-end build script.

`tequila-postgresql <https://github.com/caktus/tequila-postgresql>`_
    Install a `PostgreSQL <https://www.postgresql.org/>`_ server and
    create a project database.

`tequila-rabbitmq <https://github.com/caktus/tequila-rabbitmq>`_
    Install and configure `RabbitMQ <https://www.rabbitmq.com/>`_ to
    use as a task queue for projects that use Celery.

Additionally, work is in progress on a couple more subprojects,

`tequila-cli <https://github.com/caktus/tequila-cli>`_
    A command-line Ansible wrapper that allows referencing inventories
    and playbooks in standard locations by more compact names, and
    allows for some actions that are difficult to do in a single
    command with standard Ansible.

`tequila-dokku <https://github.com/caktus/tequila-dokku>`_
    A role that sets up a Django project under `Dokku
    <http://dokku.viewdocs.io/dokku/>`_, a `Docker
    <https://docs.docker.com/>`_ -powered Platform-as-a-Service.

Developing roles
----------------

For tips on maintaining or writing new roles for tequila, see
:ref:`tequila-role-development`.


.. toctree::
   :hidden:

   project_setup
   role_development
