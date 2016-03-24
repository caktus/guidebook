Read The Docs
=============

`Read The Docs <https://rtfd.org>`_ (RTD) publishes documentation
from open source projects on the web. For our projects that are
in git repositories and use Sphinx for their documentation, it's
often as simple as a few clicks to publish a new project's
documentation.

Accounts
--------

Either use the Caktus RTD account (credentials are shared
in LastPass), or a client account if the client prefers.

Linking to GitHub?
------------------

If the project's repository is public, you can
publish it without giving RTD any access to your GitHub
account.

Adding a project
----------------

Go to the `RTD dashboard <https://readthedocs.org/dashboard/>`_
and click the "Import a Project" button.

If the RTD account is linked to any GitHub, Bitbucket, etc
accounts, then RTD will helpfully list the repositories
it has access to that way, and you can click on one of them.

In any case, you can click "Import Manually" and enter
a name and repository URL for the project.

Versions/Branches
-----------------

You can control which branches of your project RTD builds
and publishes the documentation for. RTD calls these Versions.
Go to your project's Admin area (look for the button with the
gear and the word "Admin"), click Versions in the left-hand
navigation, and select the branches you want to build and
deselect the ones you don't.

Private projects?
-----------------

You can link the RTD account to GitHub accounts (or Bitbucket,
etc) to let it access the source of a private project, but RTD
can't really protect the built documentation from unwanted
access.

According to the RTD `privacy controls <http://docs.readthedocs.org/en/latest/privacy.html>`_,
you can set a level of "private", but it just hides the project
from lists and searches. Anyone with the URL can still view
the documentation.
