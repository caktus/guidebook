Papertrail
==========

#. Add the :ref:`forward_logs` state to your ``conf/salt/top.sls`` file. We want this to be on all
   servers so it should go in the ``*`` section:

   .. code-block:: yaml
      :emphasize-lines: 9

      '*':
      - base
      - sudo
      - sshd
      - sshd.github
      - locale.utf8
      - newrelic_sysmon
      - project.devs
      - forward_logs

#. Create a `support request <https://caktus.atlassian.net/servicedesk/customer/portal/3>`_ to get a
   Papertrail account.

#. Once you have an account, find out our Papertrail instance's `hostname and port
   <https://papertrailapp.com/systems/setup>`_.

#. Encrypt those values as a ``LOG_DESTINATION`` secret:

   .. code-block:: bash

      ~/dev/myproject$ fab staging encrypt:LOG_DESTINATION='blah.papertrail.com:12345'
      "LOG_DESTINATION": |-
        -----BEGIN PGP MESSAGE-----
        Version: GnuPG v1

        hIwDi3G8b0sD8fkBA/4kMuhn2YmdKhyy99Xi3Nn6XOUmY/oikyU1AF68ynHfywNd
        zcu8xcA0iHhj/eK7dDvC9eE94xUNNoPkddU+J6ulzhEIzQFWndD5YCO1WyHWLYbq
        N48BPaiUHWoiWFKA4aApPJHPfiV6JJUxiwHadhoAseOQw94ce75fUqbe4RiXrNJS
        ATFNQz0dtCF8H0VhYBUYHvF7yHuhZVeOqgTT93B0tDGCy9rq47Dq3PnjityrFuAL
        TLNW7zsjjEuA1P6HZ8xwRqYwSJ4MF8tkXDUX3Q++cGlW6w==
        =w3nx
        -----END PGP MESSAGE-----

#. Add that secret to your ``conf/pillar/staging.sls`` file and deploy:

   .. code-block:: bash

      ~/dev/myproject$ fab staging deploy

#. Repeat the same process for production.

#. After the deploy, you should be able to verify a couple things.

   A. All logs from gunicorn, celery and nginx (among others) should now be piped to
      ``/var/log/syslog`` on the server.

   B. You should see those same logs in the `All Systems <https://papertrailapp.com/events>`_ log.

#. Visit the `dashboard <https://papertrailapp.com/dashboard>`_ to create a new group for your
   systems, or to add them to other appropriate groups.
