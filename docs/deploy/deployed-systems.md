Deployed Architecture
=====================

Let\'s start with an overview of some typical architectures for our
deployed sites.

Note that depending on the expected traffic of a site, we might run
everything on one server, or spread services out onto different servers
(e.g. web servers, celery workers, database master, cache, etc.).

Operating system
----------------

Our server operating system of choice is Ubuntu Server LTS. For new
projects, we\'ll use the most recent LTS release.

We won\'t necessarily update projects that might be on an older LTS
release, as long as they\'re still getting security updates and we
don\'t need some feature that\'s only available on a newer release.

### System updates

We have started enabling automated updates on some projects using
Ubuntu\'s support for that. For now we\'re only enabling them for
security updates, not all software, and we\'re also blocking updates for
Salt and other packages that can be problematic if upgraded without
first testing that nothing breaks.

### Firewalls

We use `ufw` to manage the firewall on our servers, blocking all
incoming ports by default and only opening ports for the services that
server is providing.

When deploying to AWS, we can go further and set up the server security
groups so that, for example, only the load balancer can connect to our
web server ports.

### System users

We create a user on each system, named for the project. We use it to run
our Django processes and to own files and directories that need to be
written to at run-time.

On some projects though, we\'ll create a separate user to run the
processes. That user only needs write access to the media directory, and
everything else can be read-only.

Each developer who is allowed to run deploys has a user account on each
system, authorized by ssh public key, and enabled for passwordless sudo.
The deploy process connects to systems using ssh and the developer\'s
account, then uses sudo to make updates.

We typically deploy to Ubuntu, where root by default has no password,
and we don\'t set one. We also disable ssh\'ing into the systems as
root. The only way to get root access is to ssh as another user and then
use sudo.

### Software installation

For non-Python software, and the Python interpreters, we install using
[apt]{.title-ref} packages, even if we have to add a non-Canonical
repository in order to get the version we want. This means we don\'t
need to worry about configuration, arranging for services to run at
startup, etc., except where we want to change something from the default
behavior.

For Python packages/libraries, we install everything using Pip into a
virtualenv. We do not try to use the system packages for Python packages
even if they exist.

We manage our Django processes (gunicorn, celery beat, celery workers)
using supervisor. We currently [pip install]{.title-ref} supervisor
systemwide. We might change that soon, as the next Ubuntu LTS version
appears to have the most recent supervisor included as a system package.

Handling web requests
---------------------

### Load balancing

For sites that need load balancing, we typically use AWS Elastic Load
Balancer. We put the public SSL certificate on the load balancers, have
ELB accept both port 80 and port 443 requests, and forward them on the
corresponding port to our backend servers.

For sites that force SSL, the backend servers are responsible for
responding to port 80 requests with a redirect to the SSL URL of the
site.

When not on AWS, we\'ve used haproxy for load balancing and failover.

### Web server

Our servers use [nginx]{.title-ref} to receive incoming requests.
Requests not addressed to a known domain are failed immediately with a
444 status. Static files are served directly by nginx. Other requests
are proxied to gunicorn.

For sites that force SSL, requests to port 80 are redirected to the
corresponding `https` URL by nginx, and nginx adds headers such as
`Strict-Transport-Security`.

### Static files

For most projects, we serve our static files using Nginx. On some, we
store static and media files on S3 and let AWS serve them.

[This blog
post](https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/)
has more details.

### Django HTTP service

Django processes that serve HTTP requests are run using gunicorn. Nginx
proxies requests to gunicorn over a local TCP or Unix socket.

Asynchronous work
-----------------

### Django workers

For asynchronous work, we use Celery\'s worker daemon.

### Queue

We use rabbitmq to queue asynchronous work.

Misc. services
--------------

### Caching

Depending on the project, we might use memcached, redis, or both for
caching.

memcached is good for caching responses and data.

redis is good for a session store, since it\'s fast but persistent.

### Database server

We always use PostgreSQL as our database. On most sites, we run the
server on one system. On sites with high load or that need high
availability, we run replicas on other systems, and can send read-only
database requests to them to relieve traffic on the master server.

In some projects, we use Amazon RDS to host the PostgreSQL service.

### Logging

We are moving toward consolidating all of our logging into the local
syslog, and then forwarding it to a log monitoring service such as
Papertrail. That both lets us set up alerts that notify us when certain
things show up in the logs, and to have a central place to go where we
can view and search all the logs.

For processes managed by supervisor, we just configure them to log to
stdout, then have supervisor pass that to syslog. For other processes,
we either configure them to log to syslog, or use rsyslog\'s
[imfile]{.title-ref} input plugin to monitor their text log files and
pull them into syslog.

Then we can configure rsyslog to forward log messages to Papertrail.

### Monitoring

Our primary way of monitoring deployed servers is New Relic, using the
[New Relic system monitoring
agent](https://docs.newrelic.com/docs/servers/new-relic-servers-linux),
the [Python agent](http://newrelic.com/python), and sometimes the
ElasticSearch plugin.

### Email

We\'ll install postfix as a backup for outgoing mail, but usually if a
project is sending email, we\'ll configure Django to use an external
SMTP server.

### Node

For projects that use Node, we currently install v4.2 (LTS) from
deb.nodesource.com. (The Ubuntu LTS packages are way too old.)
