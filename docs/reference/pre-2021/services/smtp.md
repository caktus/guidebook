SMTP
====

By default, email is sent via Postfix on the same server housing the
Django application. This might be OK for low volume uses, but often
you'll want to use an external SMTP service (e.g. Sendgrid, Mailgun,
Postmark, SES, etc.). Some of these services offer both an SMTP server
in addition to an HTTP API. This document will describe only how to set
up the SMTP connection. If you want to use HTTP APIs, you'll need to
read the documentation for the service in question. Often there are
third party Django packages which can help with this.

Which SMTP service should I choose?
-----------------------------------

If the client doesn't require a specific SMTP service, then you'll
have to make a decision. As of January 2021, here is some info to help
you with that decision. Current Caktus team members are most familiar
with Amazon SES, Mailgun and Sendgrid.

If you need to manage bounces, try Sendgrid. Cakti who have used it on
the SAM project recommend it over Amazon SES, though I am not sure how
it compares with Mailgun.

If your project is already fully on AWS, then it might make sense to use
Amazon SES so that you can stay with one provider. It's also very
cheap. [AWS's current pricing](https://aws.amazon.com/ses/pricing/)
allows 62,000 free messages per month if you are sending from an EC2
instance, and then just $0.10 per 1000 messages after that. The
downside is that sending might be more complicated because AWS
automatically puts all projects in a "sandbox" which limits the number
of messages that can be sent, and the allowed recipients. There is a
process to remove those limits, but it is an extra step that developers
have to take.

[Mailgun](https://www.mailgun.com/pricing/) is not as cheap as SES, but
it is pretty close ($0.80 per 1000 messages). It's generally easier to
set up than SES, but you still may need to verify your domain by setting
some DNS records.

Setting up an SMTP service
--------------------------

For SMTP connections, you can either make a direct connection to the
external provider or you can send messages to your local Postfix
instance, which then relays the message to the external provider. We
will discuss both options.

### Direct SMTP connection

1.  Find the instructions page for the SMTP service that you are setting
    up. Here are some examples:
    A.  [Sendgrid](https://sendgrid.com/docs/Integrate/Frameworks/django.html)
    B.  [Mailgun](https://documentation.mailgun.com/en/latest/quickstart-sending.html#send-via-smtp)
    C.  [Amazon
        SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html#smtp-credentials-console)
    D.  [Postmark](http://support.postmarkapp.com/article/811-what-are-the-smtp-details-credentials-i-should-be-using)
2.  From those instructions you should be able to find values for some
    or all of the following Django settings. These are [explained in the
    Django
    docs](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-EMAIL_HOST),
    but a couple need clarification. `EMAIL_USE_TLS` actually means to
    establish an unencrypted connection and then use STARTTLS to convert
    to an SSL/TLS encrypted connection, while `EMAIL_USE_SSL` means to
    start right off with the SSL/TLS handshake.
    A.  `EMAIL_HOST` (string)
    B.  `EMAIL_PORT` (integer)
    C.  `EMAIL_HOST_USER` (string)
    D.  `EMAIL_HOST_PASSWORD` (string)
    E.  `EMAIL_USE_TLS` (Boolean)
    F.  `EMAIL_USE_SSL` (Boolean)
3.  Include these as environment variables (encrypting the secret ones)
    and make sure they get pulled in appropriately to Django settings.
4.  NOTE: Only one of `EMAIL_USE_TLS` and `EMAIL_USE_SSL` should be
    `True`. We currently recommend using `EMAIL_USE_TLS=True` if the
    service supports that.

### Local Postfix Relay

1.  As mentioned above, without any configuration, Django will send your
    messages to your local Postfix instance. You can therefore leave out
    all of the Django `EMAIL_*` settings from your pillar.
2.  Review the documentation from the SMTP provider and edit the Postfix
    configuration file on each of your web and worker machines as
    instructed. Here are some examples:
    A.  [Sendgrid](https://sendgrid.com/docs/Integrate/Mail_Servers/postfix.html)
    B.  [Postmark](http://support.postmarkapp.com/article/832-can-i-configure-postfix-to-send-through-postmark)
    C.  [Amazon
        SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/postfix.html)
