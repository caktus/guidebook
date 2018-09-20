Testing
=======

Best practices for testing Django projects

Writing tests
-------------

Principles
~~~~~~~~~~

Small, well-defined applications
++++++++++++++++++++++++++++++++

Small applications lend themselves to more coherent test suites. When
each application solves a specific problem, you can verify it's done
correctly with a smaller set of specific tests across that
application. A large monolithic app is much harder to test, as it
makes the lines between components less defined and the interactions
you need to test much harder to understand.

Each Django application should solve a specific problem and have well
defined boundaries. We can test those boundaries, and this helps us
both define what any one application is responsible for and also to
know what we need to test within it.

Application boundaries exist as many things:

* URLs handled by the application
* The views mapped by those URLs and the different ways they could be hit
* Public methods on Manager and Model classes
* Template tags
* Utility functions
* Application-specific Settings

It usually makes sense to roughly group these different kinds of
boundaries into different sets of test cases for each application.

Unit tests versus functional or integration tests
+++++++++++++++++++++++++++++++++++++++++++++++++

A `unit test` validates one small, specific, isolated behavior - the smaller
the better.  For example, if you were testing the ``sum`` built-in function,
you might write a series of unit tests that pass in different arguments and
see what the result is.

A `functional` or `integration` test validates a higher-level behavior,
often something visible to a user. For example, you might test that
after a user has voted on an issue, they are not allowed to vote again.

Both kinds of tests are important and should be included.
But it's important to be aware when writing a test whether it's supposed to
be a unit test or functional test. Tests that are hybrids of the two types
tend not to be very good at either role.

Coding for testability
++++++++++++++++++++++

When coding, keep testing in mind. For
example, break functionality down into small, more easily tested functions.
This is similar to the advice above to keep applications small, only on
a smaller scale.

Don't be afraid to refactor code if you find it hard to write tests for it.

Test the behavior, not the implementation
+++++++++++++++++++++++++++++++++++++++++

Try to treat the code being tested as a black box
with an API, and only test the behavior of that API, not the details
of what's inside the black box. If that's difficult, consider whether
that code's interface could be improved.

Unfortunately, it's difficult to both follow this advice, and use
techniques like mocking to isolate what's being tested. Each case
is a judgment call.

Test the failure cases
++++++++++++++++++++++

Don't just test that the code works when everything is fine.
Verify that it does something sane when problems occur.

If you're testing an API, give it invalid arguments. If you're
testing a form submission, provide bad input and make sure the
followup page has the right error messages. If you have code that
sends email, what happens if the mail server is temporarily
unreachable?  Think about how things can fail.

Use some judgment, of course. When accepting input from humans,
we can almost guarantee they won't always provide valid input, and
we definitely want to test that our code behaves reasonably. On
the other hand, you might decide that the only way your database
might be unavailable would be if there was a major problem at the
data center, in which case it's unlikely any requests can get to
your site anyway, so there's no point testing that case.

Only test your project's own code
+++++++++++++++++++++++++++++++++

There's no need to write tests in your own project that could only
fail if some code external to your project doesn't work correctly.
Assume that the Python standard library, Django, and other Python packages
you might be depending on do work correctly. It's enough work
writing comprehensive tests for your own project.

Output from tests
+++++++++++++++++

A successful test should produce no output. The test runner will
let us know if it passed. Any additional output from a successful
test is just distracting.

DRY tests
+++++++++

As for any programming, consider factoring out common code from
tests. But keep in mind that the best tests are short and simple.
If you find yourself doing a lot of refactoring, building utility
libraries, etc, the tests might be overdesigned. See if they can
be simplified.  Of course, that's not always possible.

Keep in mind that common code can easily be moved to ``setUp``
and ``tearDown``.

Also take a look at
`subtests <https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests>`_,
which are new in unittest with Python 3.4. They make it easy to run the same
test over a list of data and provide a useful result if some data passes
and other data fails.

Clean up files after tests
++++++++++++++++++++++++++

Unlike database changes, changes to files on the test system are
not automatically cleaned up after a test.

If your test is creating files explicitly, it's not hard
to clean up in the ``tearDown`` method. But when testing things
like file uploads, Django is creating files that your test is
not directly aware of. You might want to use a custom
test runner to set up a temporary media directory when testing starts
and clean it up when done. See
`MEDIA_ROOT and Django Tests <https://www.caktusgroup.com/blog/2013/06/26/media-root-and-django-tests/>`_

Debugging when tests fail
+++++++++++++++++++++++++

When a test assertion fails, sometimes it's not obvious why. Most
assertion methods have an optional argument you can use to add output
when the assertion fails. For example::

    self.assertTrue(form.is_valid(), form.errors)

will not only assert that your form is valid, but print the errors as
part of the failure message if it's not.

I wouldn't spend the time to add this kind of failure output to every assertion,
but it can be incredibly useful to add this temporarily when a test is failing
mysteriously.

Bug fixes and testing
+++++++++++++++++++++

When addressing a bug, use this workflow:

* Add a test that fails due to the bug, but should pass
  once the bug is fixed.
* Make the necessary changes to make the test pass.

This ensures that you understand the problem, that it's a real problem,
that the fix solves the problem, and that this particular bug won't come back.

Test-Driven Development
+++++++++++++++++++++++

There's a school of thought that writing tests first and then the code
to make them pass is a good way to develop all the time. It's called Test-Driven
Development.  That is a vast oversimplification, of course.

Caktus does not mandate TDD, but if you're interested, there's
a link to a whole book about it in the "Further reading" section
below.

Speeding up tests
+++++++++++++++++

A test that is too slow will not be run by developers, making it pointless.
If tests seem to be taking too long, here are some things to look for:

* In Django 1.8 and up, use the
  `--keepdb <https://docs.djangoproject.com/en/stable/ref/django-admin/#django-admin-option---keepdb>`_
  test option to re-use the test database across test runs.
* Avoid fixtures.
* Use `subtests <https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests>`_
  in Python 3.4+ to run many similar tests with a single setup and teardown.
* Mock out expensive processing that isn't the actual behavior being tested.
* See if you can move logic out of views and test it without having to call the views.
* Keep the size of test data to the minimum needed for the test.
* Model methods can sometimes be tested without ever saving the model instance
  to the database.
* Use
  `faster password hashing algorithms <https://docs.djangoproject.com/en/stable/topics/testing/overview/#speeding-up-the-tests>`_
  when testing.
* Use Continuous Integration to automatically run the whole test suite when changes are
  made, even if developers might have skipped it.
* In Django 1.8 and up, consider using
  `setUpTestData <https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.TestCase.setUpTestData>`_
  to set up your test data for an entire TestCase class one time.  Just be very careful not to
  modify any of that data during the tests.

Specific Cases
~~~~~~~~~~~~~~

How to test URLs and views
++++++++++++++++++++++++++

Unfortunately, there isn’t really a good way to separate the testing
of URL routing and the actual views, but thankfully that works out
fine in practice. When you look at a view, you should be able to
enumerate each type of request it's going to receive, and you can
probably cover each of these in a separate small test.

The test client is a very helpful utility Django provides to simulate
a specific URL being hit, to send POST or GET data along with the
request, and assert about the results usefully. The test client
returns the Response object of the view, which even carries the
context of any template rendering used in the view, which can be very
helpful in testing exactly what went into rendering the response,
without resorting to messy and error prone tests against the rendered
HTML.

Another useful tool is Django's
`RequestFactory <https://docs.djangoproject.com/en/stable/topics/testing/advanced/#the-request-factory>`_,
which can be used to create a Request object that can be passed
directly to any view, bypassing the URL routing & middleware
processes to speed things up.

If bypassing middleware completely breaks things for a particular
view, you can call specific middleware yourself on the request object first.

Nevertheless, unit testing views is hard due to how many dependencies
they introduce.
The most valuable way to help testing views is to reduce the amount of
code within views in the first place. Pushing functionality of
business data logic into models and user data into forms can reduce
most views to little more than glue connecting simpler components you
can separately test much easier.

References:

* `Django: Writing and running tests <https://docs.djangoproject.com/en/stable/topics/testing/overview/#module-django.test.client>`_

Testing forms
+++++++++++++

Testing views will inherently test some of your forms, but it's an expensive
way to do it. It's much better to do the thorough testing of your forms using
separate tests.

How to test database behaviors
++++++++++++++++++++++++++++++

Your application’s ``models.py`` should contain all of its database
interaction, and its associated test suite will need to verify these
are working properly. You need to test that query helpers, like
manager methods, are giving you the right results given expected
database contents, and that models validate, save, and are properly
updated by other helpers. All of these require tests that actually
work on a real database, because some behaviors can only be replicated
accurately with a full round trip of the SQL.

The Django test runner provides facilities that create a new database
just for the tests and run migrations to create all the tables your
applications need. Your tests can create and remove test
data in their ``setUp`` and ``tearDown`` methods, and at the end of
each test, the runner will roll back all database changes that the test
made. This can be invaluable, but also comes at a cost in test run time.

Inheriting from ``django.test.TestCase`` will run your tests in a
database transaction, and require the test database building, in order
to run the tests. Tests directly using ``unittest.TestCase``, however,
will run like any other Python unittests and avoid these extra
database tests. Distinguishing which test cases you need the database
support for can help you speed up your test run time, and also better
frame which areas of your application are responsible for database
behaviors and which are not.

Be aware, though, that if database access creeps into a test that
isn't using ``django.test.TestCase``, it will make permanent
changes to the test database and often break unrelated tests that
assume a pristine database.  This can be very hard to debug.
It's a good idea to add some protection
against this. For example, see `slide 29 of Carl Meyer's talk
on django testing <http://carljm.github.io/django-testing-slides/#29>`_
for a way to immediately cause tests to fail if they access the
database when they weren't expected to.

A note on data fixtures: Django provides a feature for adding test
data from JSON or other formats, but in practice we’ve found this to
be an impractical tool and advise against it. Problems include
difficulties updating your fixtures when data schemas and requirements
change; and the disconnect between reading your test code and your
test data. Instead, tests that create data programmatically in the
setUp() or test methods will give you tests that are easier to read,
easier to setup, and in most cases continue to function during schema
changes.

References:

* `Django: Writing and running tests <https://docs.djangoproject.com/en/stable/topics/testing/overview/>`_
* Carl J Meyer: Testing and Django `slides <http://carljm.github.com/django-testing-slides/>`_
  and `video <http://www.youtube.com/watch?v=ickNQcNXiS4>`_. Unfortunately,
  the first part (slides 2-12) is
  out-of-date with behavior of current versions of Django (1.9 as I write this), so
  skip ahead to slide 13 and continue from there.

Testing Django template tags
++++++++++++++++++++++++++++

It's easy to overlook testing any custom template tags in the project,
but they need to be tested too.  These references go into detail
about how to test template tags.

References:

* `How To Test Django Template Tags - Part 1 <http://techblog.ironfroggy.com/2008/10/how-to-test-django-template-tags-part-1.html>`_
* `How To Test Django Template Tags - Part 2 <http://techblog.ironfroggy.com/2008/10/how-to-test-django-template-tags-part-2.html>`_

What to mock and when
+++++++++++++++++++++

One of the most commonly used tools in writing Python and Django tests
these days is the mock library, which provides an extremely simple and
flexible way of faking parts of your code.

This lets you test specific areas of an application, while assuring
other pieces it depends on act correctly for the conditions you want
to test.  It also lets you run tests without depending on external
services or expensive computation that the behavior depends on
normally.

This lets your tests focus which parts of the code they actually
cover, and a failing test is a much more narrow path to the code it
alerts you to.

Good things to mock include:

* Routines which do anything with network or IO access. This also speeds up tests considerably!
* 3rd party libraries
* Other applications
* Routines depending on the time of day
* Logging (at least to test that it is happening correctly)

Similar to mocking, you can override Django settings for a single test
or test case using the
`override_settings <https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.override_settings>`_
decorator.

References:

* `Mock - Mocking and Testing Library <http://www.voidspace.org.uk/python/mock/>`_ (standalone Mock library for Python pre-3.3)
* `Testing Javascript <http://sinonjs.org/>`_
* `unittest.mock — mock object library <https://docs.python.org/3/library/unittest.mock.html#module-unittest.mock>`_ (Mock in Python 3.3+)

Factories
+++++++++

Factories are utilities that can provide random but valid test objects.
They allow test writers to focus on the important parts of the test data,
and not clutter tests with lots of other boilerplate just to end up with
valid test objects.

We typically use `Factory Boy <http://factoryboy.readthedocs.org/en/latest/>`_,
which has good Django support.

Testing the front-end
+++++++++++++++++++++

Part of testing front-end code is writing unit tests for front-end JavaScript.
For details on how to do that, see the `front-end JS docs <./frontend.html>`_.

Another part of testing is making sure the site works right in a browser. If a site
is purely HTML and CSS with no Javascript in the browser, then you can get away
with testing using the Django test client and examining the HTML in the
responses. But fewer and fewer sites run without Javascript.

`Selenium <http://www.seleniumhq.org/>`_ is a tool we can use to run a real or simulated browser,
drive interaction with our site, and verify the correct behavior.

Selenium has problems, admittedly. It's hard to write Selenium tests that
pass consistently, partly because you always have to keep in mind that
it takes time for an action taken on the test browser, like clicking
an element, to finish with whatever behavior it triggered before you can
test for it. Tests also tend to be fragile as layouts change.

But Selenium seems to be the best tool we have right now for front-end
testing.

Test cases to use for Selenium should inherit from
`LiveServerTestCase <https://docs.djangoproject.com/en/stable/topics/testing/tools/#liveservertestcase>`_,
which will arrange for a real HTTP server to be running for the test browser to make
requests to.  Follow that link for a complete example of writing a Django test
using Selenium.

Testing management commands
+++++++++++++++++++++++++++

Don't overlook testing your management commands. You can call them from tests using
`call_command() <https://docs.djangoproject.com/en/stable/topics/testing/tools/#topics-testing-management-commands>`_.

Keep in mind that the logic for a management command doesn't need to live in the
command's handler method. I often write a utility method that's part of the
project, and then the management command just calls it. That kind of management
command hardly needs testing, so long as the underlying utility is well tested.

Testing migrations
++++++++++++++++++

Do migrations need to be tested? Sometimes. Your typical "add another field" migration
probably doesn't need testing. But data migrations do need to be tested. One approach
is to migrate back to the migration preceding the migration we want to test, set up
some data, migrate forward to the migration under test, then verify the data has
been migrated correctly.

Here's a blog post with code and more detailed explanations:

`Testing Django Migrations <https://www.caktusgroup.com/blog/2016/02/02/writing-unit-tests-django-migrations/>`_.

Running tests
-------------

Discovery and Running
~~~~~~~~~~~~~~~~~~~~~

Both Django and Python’s standard library include test runners, and
there are numerous others available from the community. The most
popular third party runner is probably Nose, which also has a
Django-specific extension, django_nose.

Regardless of the runner you use, an increasingly popular step is to
run all your tests with the tox utility, which allows you to define a
number of environments you want to test and will run your test suite
across all of them. This lets you ensure a code base works correctly
not only for your local Python and Django version, for example, but
across multiple versions and combinations of versions you want to
support. Even for internal projects where you control the versions
deployed to, this can be invaluable when preparing for dependency
upgrades, such as migrating to a new Django release.

References:

* `unittest — Unit testing framework <http://docs.python.org/2/library/unittest.html>`_
* `Test Discovery <http://docs.python.org/2/library/unittest.html#test-discovery>`_
* `Nose <https://nose.readthedocs.org/en/latest/>`_
* `django-nose <https://github.com/jbalogh/django-nose>`_

Continuous Integration
~~~~~~~~~~~~~~~~~~~~~~

Continuous Integration (CI) is a term we mis-use to refer to
automatically running our test suite on our project whenever
there are changes.

See http://caktus.github.io/developer-documentation/services/travis.html
for help using Travis CI with Caktus Django projects.

Coverage
--------

With either an existing code base or a new project, you want to be
sure as much of your code as possible is being tested. Rather than
guessing, the coverage.py tool makes tracking test coverage easy. It
runs any command, usually your test runner, and creates a report of
every line of code executed, and the percentage of each module that
was actually run during your test execution. You can monitor your
project's test coverage, and make sure added new code doesn’t reduce
your coverage. A good strategy with existing code bases is to find
your current coverage rating and set this as a requirement for any new
code -- no change is allowed which reduces test coverage. Over time,
you'll your project’s code coverage to a reasonable level.

An easy approach is to use a script to run your tests::

    #!/usr/bin/env bash
    set -e

    flake8
    coverage erase
    coverage run manage.py test --keepdb "$@"
    coverage report -m --fail-under 80

Notice the ``--fail-under 80`` when generating the coverage report,
which will fail the test if coverage drops below 80%. That number can
be gradually increased over the life of the project.

References:

* `coverage tool for Python <https://pypi.python.org/pypi/coverage>`_
* `Measuring Coverage <https://django-testing-docs.readthedocs.org/en/latest/coverage.html>`_


Manual testing
--------------

In addition to automated testing, we also want to run the site and make sure it
works right from the end user's point of view. But we don't want to waste our testers'
time by asking them to test things that aren't ready yet.

When is a ticket ready for QA?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The cycle between development and QA can be very time-consuming, and the earlier bugs are caught and fixed, the less impact they will have on the project's timeline and budget. It’s up to the individual developer to define what he/she thinks is a reasonable amount of testing to do as part of code review, but here are some questions you should ask before sending a ticket to QA, in order to avoid unnecessary iterations:

* Does this feature/change load on staging, in at least 1 browser (or 1 device if on mobile)?
* Does the task/story meet all the acceptance criteria?
* Does it match the design/mockup to the expected level for the project?
* Are best practices being followed?

   * examples: interactive elements have hover states, links to external sites open in new tabs, everything is responsive!

* Are deviations from design, expected functionality, or other information needed for testing documented in JIRA?

Further reading
---------------

* Harry J. W. Percival: `Test-Driven Development With Python <http://shop.oreilly.com/product/0636920029533.do>`_
* Karen M. Tracey: `Django 1.1 Testing and Debugging <https://www.packtpub.com/web-development/django-11-testing-and-debugging>`_
