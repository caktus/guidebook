New Relic
=========

To enable New Relic monitoring for an environment:

#. Get a license key. This can be found by clicking on 'Account Settings' from the dropdown menu at
   the upper right corner of the web interface. If you don't have access to New Relic or are unsure
   of which New Relic subaccount to use, create a `support request
   <https://caktus.atlassian.net/servicedesk/customer/portal/3>`_

#. Generate an encrypted variable ``NEW_RELIC_LICENSE_KEY`` containing the license key for each
   environment:

   .. code-block:: bash

      ~/dev/myproject$ fab staging encrypt:NEW_RELIC_LICENSE_KEY='abc123'
      "NEW_RELIC_LICENSE_KEY": |-
        -----BEGIN PGP MESSAGE-----
        Version: GnuPG v1

        hIwDi3G8b0sD8fkBA/4kMuhn2YmdKhyy99Xi3Nn6XOUmY/oikyU1AF68ynHfywNd
        zcu8xcA0iHhj/eK7dDvC9eE94xUNNoPkddU+J6ulzhEIzQFWndD5YCO1WyHWLYbq
        N48BPaiUHWoiWFKA4aApPJHPfiV6JJUxiwHadhoAseOQw94ce75fUqbe4RiXrNJS
        ATFNQz0dtCF8H0VhYBUYHvF7yHuhZVeOqgTT93B0tDGCy9rq47Dq3PnjityrFuAL
        TLNW7zsjjEuA1P6HZ8xwRqYwSJ4MF8tkXDUX3Q++cGlW6w==
        =w3nx
        -----END PGP MESSAGE-----

#. Put that in the proper environment's SLS file, in the ``secrets`` dictionary:

   .. code-block:: yaml

      # <environment>.sls
      secrets:
        NEW_RELIC_LICENSE_KEY: |-
          -----BEGIN PGP MESSAGE-----
          -----END PGP MESSAGE-----

#. Add any other custom `New Relic configuration variables
   <https://docs.newrelic.com/docs/agents/python-agent/installation-configuration/python-agent-configuration#environment-variables>`_
   under ``env:``. The default values will probably work well for most projects, but if you want to
   change them, here are some examples:

   .. code-block:: yaml

      # project.sls
      env:
        NEW_RELIC_LOG: "/var/www/myproject/log/agent.log"
        NEW_RELIC_MONITOR_MODE: "false"

      # <environment>.sls
      env:
        NEW_RELIC_APP_NAME: myproject <environment>
        NEW_RELIC_MONITOR_MODE: "true"

   Be sure to quote "true" and "false" as above, to avoid Salt/YAML turning these into real Booleans;
   we want the strings "true" or "false" in the environment.

   You can put some values in ``project.sls`` and others in ``<environment>.sls``.  Just be
   consistent for a given key; if the same key is present in both ``project.sls`` and the current
   ``<environment>.sls`` file, Salt makes no guarantees about which value you'll end up with.

   Note that any environment where ``NEW_RELIC_LICENSE_KEY`` is not set will not include any New
   Relic configuration, so it's safe to put other settings in ``project.sls`` even if you're not
   using New Relic in every environment.

#. If you are using elasticsearch and would like New Relic monitoring of that as well, add to the
   pillar somewhere.

   .. code-block:: yaml

      # project.sls or <environment>.sls
      elasticsearch_newrelic: true

   The plugin will get setup automatically if that pillar setting is present, and you are
   using the ``elasticsearch`` margarita state in your ``top.sls`` file.

#. Add state ``newrelic_sysmon`` to your Salt ``top.sls`` in the ``base`` section (for all servers).
   It's safe to add that unconditionally for all environments; it's a no-op if no New Relic
   license key has been defined:

   .. code-block:: yaml

      base:
        '*':
          - ...
          - newrelic_sysmon

#. Be sure ``newrelic`` is in the Python requirements of the project (likely in
   ``requirements/production.txt``): https://pypi.python.org/pypi/newrelic
