Django Project Template Testing Plans
=====================================

Caktus relies on our [Django Project
Template](https://github.com/caktus/django-project-template/) which we
roll improvements into when we learn new best practices in a project
that we want to make part of our baseline. Unfortunately, testing
changes to this project template is prohibitively difficult. The
template itself is not a project that can be run, because it is only a
valid project after the Django `startproject` command has processed it.

We have developed both some improvements to the template and a plan for
further improvements. You will find both of these documented here.

Testing Changes
---------------

If you make any change to the project template you'll need to test it
before submitting a pull request and you'll want reviewers of your pull
request to be able to test it consistently, as well.

To test changes, you'll want to use the `startproject` command to
create a new test project based on your current changes. Run this from
the same directory you have your local copy of hte template.

    django-admin.py startproject 
      --template=django-project-template 
      --extension=py,rst,yml 
      --name=Makefile,gulpfile.js,package.json
      dpttest

If this was successful, continue setting up this temporary project to
ensure your changes did not break the setup and utilization of a new
project based on the template.

    cd dpttest
    make setup
    workon dpttest
    npm run dev

You should be able to bring up a blank page at
[http://localhost:8000/](http://localhost:8000) successfully.

If you've made changes affecting deployment, you should also test this
by following the vagrant setup instructions in this test project.

When you are done testing, you should clean up the project.

    cd ..
    deactivate
    rm -rf dpttest
    dropdb dpttest
    rmvirtualenv dpttest

Future Improvements
-------------------

The changes that make testing the project template faster are a start,
but there's still a lot we can do to make this process better in the
future.

### Automation

Spinning up a temporary project from the template, running the server
and test suite, and cleaning everything up is something that could be
automated into a simple testing tool. This is something that would have
to live outside the project template itself as its own small tool.

This would benefit us the most if it included testing provision and
deploy to a new vagrant box, and cleaned that box up as well.

### Expanding Testable Surface

Right now it is feasible to do basic tests that a new project from the
template can be setup and runs, but that doesn't really exercise a lot
about the setup. It would be ideal if we could perform deeper
integration testing on the components we rely on, such as the database,
cache, and celery.

Our current proposal is to include a new app in the template that Caktus
would maintain: a Django healthcheck app. This would serve up a
predictable view that, when hit, would run a series of integration tests
to verify the setup of a server was correct. It would perform operations
on the database, write and read against memcache, and verify tasks sent
to celery completed properly.

This is an app that would be valuable for existing projects, but that
also would make a much more complete verification of the infrastructure
the template (and Margarita) sets up is configured correctly.
