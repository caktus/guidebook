Upgrading Django
================

Django routinely releases new versions containing bug and
security fixes, and not infrequently new major versions with
interesting new features that we want to use.

Upgrading an existing project to use a newer version of
Django is always a little different, but there are some
principles that are almost always helpful.

One major version at a time
---------------------------

If you're multiple major versions behind, do the Django upgrade one
major version at a time, working through all the upgrade notes for
one release and resolving all issues before moving on to the
next Django major version.

It's okay to jump straight to the last available minor release
of a major version though.

Release notes
-------------

Even for minor Django upgrades, you should always read the
release notes.

They don't make these easy to find, but they're consistently linked
to from the very last line of the table of contents for that major
version's documentation. E.g. for 1.9.x releases, go to
https://docs.djangoproject.com/en/1.9/, scroll all the way to the
bottom, and in the last line in the page body (ignoring the page
footer), there's a link to "Release notes and upgrading instructions".

The check command
-----------------

The command ``python manage.py check`` is great for pointing
out possible incompabilities.  Run it before upgrading, fix
any reported issues, then run it again after upgrading and fix
any new issues.

Another handy one is ``python manage.py check --deploy``.
It suggests ways to improve your settings for greater security,
including ways to enable new security features that might be
available after upgrading.

Testing
-------

Run your tests before and after upgrading. Fix any deprecation
warnings before upgrading. Fix any new ones after upgrading.
And of course, fix any test failures.

There's an environment variable you can set that will
turn particular warnings into errors. My current setting
looks like this; adapt as needed::

    export PYTHONWARNINGS=error:RuntimeWarning,error:RemovedInDjango18Warning,\
    error:RemovedInDjango19Warning,error:RemovedInDjango110Warning

(all one long line)

Third party packages
--------------------

For major version upgrades of Django, it's almost inevitable that
you'll have to upgrade at least some third-party packages as well.
Some, like ``django-debug-toolbar``, seem to need upgrading almost
every time.

This is where a complete test suite is invaluable to find these
problems before deploying.

Once I identify that a problem seems to be caused by a third-party
package, I typically just ``pip install -U package-name`` and
try the test again. If that fixes it, I look to see what version
of the package I ended up with, and update the requirements file
to that version. Otherwise I head for the third-party package's
documentation, and sometimes their issue tracker, to see if I can
find more information on the problem.
