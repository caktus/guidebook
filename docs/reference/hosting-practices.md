Hosting best practices
======================

When we're responsible for a site staying up, here are some things to
consider.

Backups
-------

At least the database and any Django media files should be backed up
daily.

Some sites might need to back up other files in order to recover from a
complete failure, case by case. For example, they might have "static"
files that aren't in the project source repository but come from some
other source.

Our projects almost always have their configuration under source control
using some form of configuration management, so backing up configuration
files should *not* be necessary. But a few projects might be exceptions
to this.

The Caktus sysadmin team generally takes responsibility for setting up
automatic backups, archiving them, and monitoring the backup process,
with help from the developers as needed.

Developers should be sure they know how to go from backups to running
servers. Furthermore, you can't really know if you can do this unless
you've done it, so we should practice disaster recovery for each
project where that would be critical in an emergency.

Notification on errors
----------------------

We need to know when users are hitting problems on the site, or tasks
are failing, without having to manually check logs.

Sentry has been a good solution for us. It hooks into Python logging and
can send notifications when errors happen.

One excellent feature is that it doesn't send a separate notification
for every occurrence of what looks like the same error, so when
something goes wrong, nobody ends up with hundreds or thousands of
emails about it.

[TODO: step-by-step setup]

Logging
-------

When something fails, it can be helpful to see all the logs, not just
the message that triggered the notification. It can also be helpful to
see logs from more than just Django - e.g. the web server, cron jobs,
database, whatever.

For that reason, we will sometimes arrange to send as many logs as
possible to [Papertrail](http://papertrailapp.com), which makes it easy
to see all the messages in context, filter and search, and even set up
alerts that can look for more complicated triggers than just whether a
message was an "error".

[TODO: step-by-step setup]

[for Dokku: If you need to set that up on a new server, you'll need
the Papertrail URL which you can find by going to the [Papertrail Setup
page](https://papertrailapp.com/systems/setup) in your account. It
should look something like `syslog+tls://logs5.papertrailapp.com:12345`
where the numbers will be different:

    $ ssh dokku logspout:server <papertrail-log-url>
    $ ssh dokku logspout:start

Monitoring
----------

Monitoring is to let us know quickly when something is seriously wrong
on the site, or heading that way. For example, if the site won't load
at all, or response time is getting very slow, or resources are running
out on servers (CPU, memory, disk, etc).

The New Relic free account level provides for site outage or slow
response monitoring (look under "Synthetics" in the web UI).

QUESTION - can we set up resource usage monitoring under NR free
accounts? (e.g. if disk space is almost gone, or CPU is high, etc?)

[TODO: step-by-step setup]

Updates
-------

We typically set up security updates to happen automatically on our
servers, but not necessarily all updates. For a site where the cost of
an unexpected outage would be low, we might accept the risk of applying
all updates automatically rather than having to do it ourselves from
time to time. We likely don't want to do that if an unexpected outage
would be expensive.

[TODO: step-by-step setup]
