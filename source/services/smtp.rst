SMTP
====

By default, email is sent via Postfix on the same server housing the Django application. This might
be OK for low volume uses, but often you'll want to use an external SMTP service (e.g. Sendgrid,
Mandrill, Postmark, SES, etc.). Some of these services offer both an SMTP server in addition to an
HTTP API. This document will describe only how to set up the SMTP connection. If you want to use HTTP
APIs, you'll need to read the documentation for the service in question. Often there are third party
Django packages which can help with this.

For SMTP connections, you can either make a direct connection to the external provider or you can
send messages to your local Postfix instance, which then relays the message to the external
provider. We will discuss both options.

Direct SMTP connection
----------------------

#. Find the instructions page for the SMTP service that you are setting up. Here are some examples:

   A. `Sendgrid <https://sendgrid.com/docs/Integrate/Frameworks/django.html>`_
   #. `Mandrill <https://mandrillapp.com/settings/index>`_ (Need to be logged in to see.)
   #. `Postmark
      <http://support.postmarkapp.com/article/811-what-are-the-smtp-details-credentials-i-should-be-using>`_

#. From those instructions you should be able to find values for some or all of the following Django
   settings. These are `explained in the Django docs
   <https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_HOST>`_, but a couple need
   clarification. ``EMAIL_USE_TLS`` actually means to establish an unencrypted connection and then
   use STARTTLS to convert to an SSL/TLS encrypted connection, while ``EMAIL_USE_SSL`` means to
   start right off with the SSL/TLS handshake.

   A. ``EMAIL_HOST`` (string)
   #. ``EMAIL_PORT`` (integer)
   #. ``EMAIL_HOST_USER`` (string)
   #. ``EMAIL_HOST_PASSWORD`` (string)
   #. ``EMAIL_USE_TLS`` (Boolean)
   #. ``EMAIL_USE_SSL`` (Boolean)

#. Set these variables in ``conf/pillar/<environment>.sls``. Some of these might be OK to be public,
   and those can go in the ``env:`` dictionary. If they are private, they should be encrypted and
   then placed in the ``secrets:`` dictionary. Include only the variables that your service needs.

   .. code-block:: bash

      ~/dev/myproject$ fab staging encrypt:EMAIL_HOST_PASSWORD='password-provided-by-smtp-service'
      "EMAIL_HOST_PASSWORD": |-
        -----BEGIN PGP MESSAGE-----
        Version: GnuPG v1

        hIwDi3G8b0sD8fkBA/4kMuhn2YmdKhyy99Xi3Nn6XOUmY/oikyU1AF68ynHfywNd
        zcu8xcA0iHhj/eK7dDvC9eE94xUNNoPkddU+J6ulzhEIzQFWndD5YCO1WyHWLYbq
        N48BPaiUHWoiWFKA4aApPJHPfiV6JJUxiwHadhoAseOQw94ce75fUqbe4RiXrNJS
        ATFNQz0dtCF8H0VhYBUYHvF7yHuhZVeOqgTT93B0tDGCy9rq47Dq3PnjityrFuAL
        TLNW7zsjjEuA1P6HZ8xwRqYwSJ4MF8tkXDUX3Q++cGlW6w==
        =w3nx
        -----END PGP MESSAGE-----

#. NOTE: Only one of ``EMAIL_USE_TLS`` and ``EMAIL_USE_SSL`` should be ``True``.

#. Here is an example ``conf/pillar/staging.sls`` file:

   .. code-block:: yaml

      env:
        EMAIL_HOST: 'smtp.postmarkapp.com'
        EMAIL_PORT: 587
        EMAIL_USE_TLS: True

      secrets:
        EMAIL_HOST_USER: |-
          -----BEGIN PGP MESSAGE-----
          -----END PGP MESSAGE-----
        EMAIL_HOST_PASSWORD: |-
          -----BEGIN PGP MESSAGE-----
          -----END PGP MESSAGE-----


Local Postfix Relay
-------------------

#. As mentioned above, without any configuration, Django will send your messages to your local
   Postfix instance. You can therefore leave out all of the Django ``EMAIL_*`` settings from your
   pillar.

#. Review the documentation from the SMTP provider and edit the Postfix configuration file on each
   of your web and worker machines as instructed. Here are some examples:

   A. `Sendgrid <https://sendgrid.com/docs/Integrate/Mail_Servers/postfix.html>`_
   #. `Mandrill
      <https://mandrill.zendesk.com/hc/en-us/articles/205582187-How-to-Use-Postfix-to-Send-Email-with-Mandrill>`_
   #. `Postmark
      <http://support.postmarkapp.com/article/832-can-i-configure-postfix-to-send-through-postmark>`_
   #. `Amazon SES <https://docs.aws.amazon.com/ses/latest/DeveloperGuide/postfix.html>`_

#. We currently don't have support for making these configuration changes in Margarita, so these
   need to be done manually.
