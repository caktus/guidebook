Upgrading Django
================

Django routinely releases new versions containing bug and security
fixes, and not infrequently new major versions with interesting new
features that we want to use.

This document outlines:

-   some principles that that we have found helpful when upgrading
    Django
-   a list of steps that we have used when upgrading Django on different
    projects

Helpful Principles
------------------

### Upgrade from LTS version to LTS version

Django\'s deprecation policy makes it manageable to upgrade from one
long-term support (LTS) release to the next LTS release. We recommend
first upgrading to an LTS release, then fixing the deprecation warnings
on that LTS release, then working on upgrading to the next LTS release.
For the Django roadmap of LTS releases, see
<https://www.djangoproject.com/weblog/2015/jun/25/roadmap/>.

### Release notes

Even for minor Django upgrades, you should always read the release notes
for the new features, as well as the new deprecations. For release
notes, see <https://docs.djangoproject.com/en/dev/releases/>.

### The check command

The command `python manage.py check` is great for pointing out possible
incompatibilities. Run it before upgrading, fix any reported issues,
then run it again after upgrading and fix any new issues.

Another handy one is `python manage.py check --deploy`. It suggests ways
to improve your settings for greater security, including ways to enable
new security features that might be available after upgrading.

### Testing

Run your tests before and after upgrading. Fix any deprecation warnings
before upgrading. Fix any new ones after upgrading. And of course, fix
any test failures.

There\'s an environment variable you can set that will turn particular
warnings into errors. My current setting looks like this; adapt as
needed:

    export PYTHONWARNINGS=error:RuntimeWarning,error:RemovedInDjango18Warning,\
    error:RemovedInDjango19Warning,error:RemovedInDjango110Warning

(all one long line)

### Third party packages

For major version upgrades of Django, it\'s almost inevitable that
you\'ll have to upgrade at least some third-party packages as well.
Some, like `django-debug-toolbar`, seem to need upgrading almost every
time.

This is where a complete test suite is invaluable to find these problems
before deploying.

Once I identify that a problem seems to be caused by a third-party
package, I typically just `pip install -U package-name` and try the test
again. If that fixes it, I look to see what version of the package I
ended up with, and update the requirements file to that version.
Otherwise I head for the third-party package\'s documentation, and
sometimes their issue tracker, to see if I can find more information on
the problem.

Recommended Steps:
------------------

We recommend following these steps when upgrading Django versions:

1.  Check out Django\'s [release
    notes](https://docs.djangoproject.com/en/dev/releases/) for the
    newer. version. For instance, the release notes for Django2.0 can be
    found here: <https://docs.djangoproject.com/en/dev/releases/2.0/>.
    If there is anything from the notes that clearly needs to be updated
    (a certain function is deprecated, etc.), make those updates to the
    code. Don\'t worry about catching everything (sometimes there\'s not
    anything that sticks out from the notes).
2.  Determine if our code generates any deprecation warnings by running
    the test suite. Use the `-W` command line argument to show the
    deprecation warnings. Adding `once` after `-W` will only show the
    first occurrence of each warning in order to make seeing the
    warnings more manageable:

        python -Wonce manage.py test

    A deprecation warning will look like:

        /Users/username/projects/coolproject/coolapp/models.py:65: RemovedInDjango20Warning: on_delete will be a required arg for ForeignKey in Django 2.0. Set it to models.CASCADE on models and in existing migrations if you want to maintain the current default behavior. See https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.ForeignKey.on_delete
        category = models.ForeignKey(Category)

3.  If our code has deprecation warnings, then make the changes there.
    If one of our dependencies has deprecation warnings, then look into
    whether a newer version of the dependency is available, and try to
    upgrade that first. It may be helpful to make a few or just 1 change
    at a time, rather than trying to do everything at once. Assuming
    that thorough tests have been written for our application, feel free
    to run the test suite after each set of changes to make sure that
    everything still runs. Sometimes things will break unexpectedly and
    you will need to determine why. Googling the error messages is
    oftentimes helpful in such a situation.

    Note: if you upgrade a dependency, make sure you update
    `requirements.txt` with the newer version of the dependency, as well
    as newer versions of sub-dependencies. For example, if you update
    the `celery` dependency, and this upgrade also upgrades the `pytz`
    sub-dependency, then pin down both the `celery` version and the
    `pytz` version in the appropriate requirements file.

    It may also be a good idea to review our dependencies even if they
    don\'t generate deprecation warnings. Feel free to upgrade
    dependencies to newer versions and to run the test suite to make
    sure the upgrade didn\'t break anything, and make sure to update the
    version number in appropriate requirements file. You can see which
    dependencies have newer releases by running:

        pip list --outdated

    and see the same list in a column format with:

        pip list --outdated --format=columns

4.  Once all of the deprecation warnings have been resolved, update the
    requirements file with the new version of Django and run
    `pip install -r requirements.txt`.
5.  Try to run the server locally (with `npm run dev`, or
    `python manage.py runserver`, or whatever is relevant for your
    project), and navigate to the site locally. If something is broken,
    look into fixing it.
6.  Once everything seems to run locally, run the test suite and make
    sure all of the tests pass. If something is broken, look into fixing
    it.

    Note: sometimes you may need to fix the test, rather than the
    non-test code, especially if something works in the browser, but
    fails in the tests. The tests are always supposed to look like the
    real environment, rather than the other way around.

7.  Make a pull request with your changes and ask another developer to
    review them. It is always important to have others review our work
    to make sure we have done it correctly and thoroughly.
8.  Deploy the code to the staging server and verify that everything
    works as it should.
