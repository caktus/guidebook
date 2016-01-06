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
