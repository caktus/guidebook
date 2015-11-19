Using Amazon RDS
================

This is how we host Postgres databases on Amazon RDS.

Policies
~~~~~~~~

RDS instances
-------------

* We host each client's data on RDS instances under the client's own AWS account.
  Different clients' data is never hosted on the same RDS instance.

* We use RDS instances in the same region as the servers that will access them.

* We use separate instances for staging and production. (Typically, the staging
  instances can be smaller.)

* We need a different RDS instance for each Postgres version we are using.

* We can host multiple sites' and projects' data for the same client
  on the same RDS instance, as long as the preceding requirements are met.

Postgres users
--------------

Each RDS instance has a master Postgres user created by AWS when the RDS
instance is created. We store the credentials for that user in Lastpass, in a shared
folder associated with the corresponding client.

For each site or project, we create a separate Postgres user used for accessing
its databases, that does not have privileges to create databases or users, or to
access other databases. (The goal is that even if a server of that site or project
is compromised, there should not be any credentials on that server that could
access any other site's or project's data, or mess up anything else on the RDS
instance.)

We also store each of these separate Postgres user's credentials in Lastpass
in a shared folder associated with the corresponding client and
project.

If a single site/project uses multiple databases, it is up the developers' discretion
whether to set up multiple users or a single user. However, using multiple users from
the same site does not appear to add any security over using a single user, since all
the credentials in use will be available on the servers.

Security and access to RDS servers
----------------------------------

We configure RDS servers to not be accessible from the Internet,
but only from the EC2 instances hosting the servers that need to access
them when running. That can be done by putting the EC2 servers in a
common security group, and setting up the RDS server's security group to
only allow port 5432 access from the EC2 servers' security group.

This implies that developers and admins will not be able to do Postgres
administration from their own machines, but will have to ssh to one of
the permitted EC2 instances and do it from there.

Provisioning databases for projects
-----------------------------------

When we're deploying a project that hosts its own Postgres server, often we'll
create the database user and database for the project during the initial deploy.
We will not be able to do that when the database is on RDS, as the deploy
will not have the credentials of the master Postgres user.

So, we create the database user and database manually (or using
some separate bit of automation).  And that will need to be done from one of
the EC2 instances. One approach would be to ssh into one of the servers and
use the Postgres command line interface. Just be careful not to leave any
credentials for the master user on that server. (If you want to be especially
careful, use a temporary EC2 instance just for that, and destroy it when done.)

See below for some detailed documentation on using the Postgres command
line to do the things that will need to be done.

Backups
-------

TBD!

(Do we just rely on the automatic backups on RDS, which are only kept up
to 45 days; do we make "manual" (initiated when we choose) backups on RDS,
which will be kept as long as we want; or do we want to make backups
outside of RDS?)

Practical tips
~~~~~~~~~~~~~~

Before starting to work with RDS, read or at least skim through
`the AWS documentation on how Postgres works on RDS
<http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html>`_,
and pay special attention to
`Appendix: Common DBA Tasks for PostgreSQL <http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.html>`_.

It'll save you a lot of headaches in the long run.

Postgres on RDS
---------------

The master user that RDS gives you is *not* a Postgres superuser. Though it
has a lot of permissions, there are a few things that you just won't be able
to do quite the way you could if you were a superuser.

In the examples below, for readability I'm omitting most of the common
arguments to specify where the Postgres server is, what the database name is,
etc. You can set some environment variables to use as defaults for things::

    $ export PGDATABASE=dbname
    $ export PGHOST=xxxxxxxxx
    $ export PGUSER=master
    $ export PGPASSWORD=xxxxxxxxxx

PGPASSWORD behaves the same as password connection parameter. Use of this
environment variable is not recommended for security reasons (some operating
systems allow non-root users to see process environment variables via ps);
instead consider using the ~/.pgpass file (see Section 30.14 of the PG docs).

Create user
-----------

This is pretty standard.  To create user ``$username`` with plain text password
``$password``::

    $ export PGUSER=master
    $ export PGDATABASE=postgres
    $ createuser -DERS $username
    $ psql -c "ALTER USER $username WITH PASSWORD '$password';"

Yes, none of the options in ``-DERS`` are strictly required, but if you don't
mention them explicitly, createuser asks you about them one at a time.

Create database
---------------

If you need a database owned by ``project_user``, you'll need
to create it as ``master`` and then modify the ownership and permissions::

    $ export PGUSER=master
    $ createdb --template=template0 $dbname
    $ psql -c "revoke all on database $dbname from public;"
    $ psql -c "grant all on database $dbname to master;"
    $ psql -c "grant all on database $dbname to $project_user;"

If you need to enable extensions etc, do that now (see below).  When done, then::

    $ psql -c "alter database $dbname owner to $project_user;"

A superuser could create the database already owned by a specific user,
but RDS's master user cannot.

PostGIS
-------

To enable PostGIS, as the master user::

    $ export PGUSER=master
    $ psql -c "create extension postgis;"
    $ psql -c "alter table spatial_ref_sys OWNER TO $project_user;"

where ``$project_user`` is the postgres user who will be using the database.

(Outside of RDS, only a superuser can use ``create extension``; RDS has special
handling for a whitelist of extensions.)

Hstore
------

Hstore is simpler, but you still have to use the master user::

    $ export PGUSER=master
    $ psql -c "create extension hstore;"

Grant read-only access to a database
------------------------------------

    $ psql -c "GRANT CONNECT ON DATABASE $dbname TO $readonly_user;"
    $ psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA PUBLIC TO $readonly_user;" $dbname


Restore a dump to a new database
--------------------------------

Create the database as above, including changing ownership to the project
user, and enabling any needed extensions. Then as the project user::

    $ export PGUSER=$project_user
    $ pg_restore --no-owner --no-acl --dbname=$dbname file.dump

Note that you might get some errors during the restore if it tries to create
extensions that already exist and that kind of thing, but those are
harmless. It does mean you can't use ``--one-transaction`` or
``--exit-on-error`` for the restore though, because they abort on
the first error.

Dump the database
-----------------

This is pretty standard and can be done by the project user::

    $ export PGUSER=$project_user
    $ pg_dump --file=output.dump --format=custom $dbname

Drop database
-------------

When it comes time to drop a database, only master has the permission, but
master can only drop databases it owns, so it takes two steps.  Also,
you can't drop the database you're connected to, so you need to connect
to a different database for the ``dropdb``.  The ``postgres`` database is
as good as any::

    $ export PGUSER=master PGDATABASE=postgres
    $ psql -c "alter database $dbname owner to master;"
    $ psql -c "drop database if exists $dbname;"

(Outside of RDS, a superuser can drop any database. A superuser still
has to be connected to some other database when doing it, though.)

Drop user
---------

This is standard too.  Just beware that you cannot drop a user if anything
they own still exists, including things like permissions on databases.

    $ export PGUSER=master
    $ dropuser $user
