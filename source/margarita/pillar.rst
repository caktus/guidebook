Salt Pillar
===========

State-specific configuration is documented with each SLS file.

Global configuration
--------------------

These are variables you must set in the pillar that aren't
specific to any particular state.

* ``project_name`` - short name of the project. Used all over the place,
  e.g. to generate directory names, user names, database names, etc.  So
  should be a valid identifier.

  Most project files will end up under ``/var/www/<project_name>``.

* ``domain`` - main hostname of the project site.  This is the hostname
  that nginx etc. will expect to see on incoming requests for this site.

Setting variables in pillar
---------------------------

You can use any approach to set variables in the Salt pillar
that Salt Stack supports. But we do have some conventions we tend
to follow in our projects.

In the pillar directory (e.g. ``conf/pillar``), we start with a
``top.sls`` file like this::

    base:
      "*":
        - project
        - devs
      'environment:local':
        - match: grain
        - local
      'environment:staging':
        - match: grain
        - staging
      'environment:production':
        - match: grain
        - production

Here's what that does:

* Read ``conf/pillar/project.sls`` for all environments. This is a good
  place to put global variables like ``project_name`` and software
  versions.

* Read ``conf/pillar/devs.sls`` for all environments. We conventionally
  set ``users`` here to the list of accounts to create on the servers, but
  we could just as well set ``users`` differently per environment by moving
  the definition of ``users`` to an environment-specific file.

* Read ``conf/pillar/<environment>.sls`` depending on what environment
  we're in. This is where we put environment-specific variables, like
  what branch of our project we want to install (e.g. ``develop`` on
  staging and ``master`` on production, or whatever).
