Choosing a deploy strategy
==========================

Different projects at Caktus use different tools and strategies
for provisioning and deploying. This is partly for historical reasons,
but also because different projects have different requirements.

Strategies that manage most of the details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simple Fabric
-------------

For some of our earliest projects, we just did everything in a
`Fabric <http://www.fabfile.org/>`_
script, without the assistance of any other tools. That's error-prone
and a lot of work. We would never do that for a new project, and I'm
not sure any project we still maintain does that.

FabulAWS
--------

`FabulAWS <https://fabulaws.readthedocs.io/en/latest/>`_
is a Caktus-developed (primarily Tobias) framework
for deploying autoscaling, redundant projects to Amazon Web Services.
Its primary advantage is built-in support for autoscaling: adding and
removing servers as the load on the site changes.

Two projects use FabulAWS that I'm aware of: CCSR and OpenDebates. Both
can experience heavy loads at times, with significant load changes over
time.

These days,
`Elastic Beanstalk <https://aws.amazon.com/elasticbeanstalk/>`_
is a credible alternative to FabuLAWS.
It also supports autoscaling, using the same underlying AWS mechanisms
as FabulAWS, and we're not responsible for maintaining
it ourselves.

Both FabulAWS and Elastic Beanstalk are tied to AWS.

Margarita
---------

Most of our current client projects use a Caktus project called
`Margarita <http://caktus.github.io/developer-documentation/margarita/margarita.html>`_
for deployment, which uses the
`Salt <https://saltstack.com/>`_ configuration management system
to deploy the site.

This has worked reasonably well (well enough that we keep using it), but
over time we've discovered a number of shortcomings:

* Difficulty debugging deploy problems
* Fragility of Salt updates - many new updates seem to introduce new
  bugs, and the next update that fixes those might have its own new
  bugs. It can be tricky figuring out a version of Salt that works.
* Resource usage - the Salt master process seems to grow over time to
  use a lot of memory on the server, even though it shouldn't be doing
  anything at all when we're not deploying. This ties up memory our
  site could be using.

Tequila
-------

Tequila (see `tequila-*` projects on Caktus github)
is a successor project to Margarita, which uses
`Ansible <http://docs.ansible.com/>`_
instead of Salt. It is hoped that Tequila will avoid some of the problems
of Margarita.

* Ansible error messages are much clearer, making debugging deploy problems
  easier.
* Ansible is agent-less, so when not deploying, it takes no resources on
  the servers.
* Ansible seems (so far) to have a better track record of not introducing
  regressions with its updates.

At present, Tequila is in a beta state, with several newer projects trying
it out.

Strategies that try to abstract away some of the details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Elastic Beanstalk
-----------------

`Elastic Beanstalk <https://aws.amazon.com/elasticbeanstalk/>`_
is an AWS service that provides a nice front-end wrapper
around some of their other services, including Elastic Load balancer and
autoscaling. A `Caktus blog post <https://www.caktusgroup.com/blog/2017/03/23/hosting-django-sites-amazon-elastic-beanstalk/>`_ gave a quick overview.

A big advantage of EB over Margarita, Tequila, and FabulAWS is that it provides
a *higher level of abstraction*, so developers don't have to concern themselves
with as many details about the deploy when they just want something that works.

We inherited one project that was already using Elastic Beanstalk and have
had good experiences with it. It was a big enough project that we were grateful
for the horizontal scaling (multiple web servers behind a load balancer), and the
autoscaling currently ramps servers up and down during each day as traffic levels
vary.

We have not yet worked out a simple way to use something like Celery (background
tasks) with Elastic Beanstalk. There doesn't seem to be a simple way to run
something only on one server.

If you needed to dig down into the details more, for example to change which
web server is used, you might find it more work to do than with a strategy
that always exposes all the details.

Elastic Beanstalk is tied to AWS.

Heroku
------

We've had a few projects use `Heroku <https://heroku.com>`_.
Heroku is a well-designed and robust service
that makes it easy to deploy projects to the Internet. It provides for easy
deploy and scaling like Elastic Beanstalk. The only drawback is that running a
site on Heroku incurs a premium cost compared to the run-time costs of most of
these other alternatives. Of course, that does not take into account the high
cost of our own labor in developing and maintaining some of these other solutions.
Still, we haven't used Heroku much. Mostly we use it for quick prototypes, or
if a client specifically requests it.

Dokku
-----

`Dokku <http://dokku.viewdocs.io/dokku/>`_
is an open-source alternative to Heroku. It takes the same approach to
deploys, but doesn't (yet) offer all the services of Heroku. We are currently
trialing Dokku with some internal projects and one client project.

The advantage of Dokku is that most of the complication of implementing
and maintaining support for all the details needed in a deploy are not our
responsibility, as they are with our Salt, Ansible, and FabulAWS frameworks.
So we would spend fewer of our hours keeping up the deploy machinery.

Dokku appears best suited to smaller projects, ones where we'd be comfortable
running on a single server.

That's just because it manages things on a per-server
level, though; there's no inherent reason you couldn't run multiple servers behind
a load balancer, with each server managed using Dokku. Dokku itself just doesn't
help you there. (It might not even be that hard to use Ansible to manage a set
of identical dokku servers plus a load balancer; maybe a Shipit Day project?)

Choosing a deploy strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~

As of this writing (June 2017), here's how I'd recommend choosing a strategy:

.. code-block:: text

    If the client has a specific request for a strategy and it's feasible
        Use that

    If the project already uses a deploy strategy and it's working okay
        Keep using it

    If it's a small project (single server) with no unusual requirements,
    or no autoscaling is needed:
       If you need something that we know works reasonably well, use Margarita
       If you're willing to beta test a newer strategy, consider Tequila or even Dokku

    Else if AWS is an option
        If Elastic Beanstalk meets the project's needs
            Use Elastic Beanstalk
        Else
            Use FabulAWS, possibly customizing it for the project

    Else
        Come up with something new because we've run out of options

This should come up with something for most projects. We'd only have trouble
if we had a project needing a lot of scaling that couldn't use AWS for some
reason.
