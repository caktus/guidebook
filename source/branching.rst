Branching Strategy
==================

We use git, which is a distributed code repository where every clone is an equal citizen.
This can create issues unless the team agrees on a branching strategy.

We use a combination of long-term and short-term branches, and recognize origin as the "central" repository.
This approach is neatly summarized in the blog post `A successful Git branching model
<http://nvie.com/posts/a-successful-git-branching-model/>`_ by Vincent Driessen.

The following branching strategy is based on Vincent Driessen's outline. Under this strategy,
all developers pull and push from a shared remote server named ``origin``. For most projects this
shared remote server is hosted on Github and that is the assumption throughout this documentation.
The central repo holds two main branches with an infinite lifetime, called ``develop`` and ``master``.

``origin/master`` is always the production-ready version of the code. When a repository first starts,
it will not have a ``master`` branch until the first release. From then on, ``master`` has an infinite lifespan.

``origin/develop``, as much as possible, should be a stable version of new features, code enhancements,
and non-critical bugfixes that are intended to be merged into ``origin/master``.

By merging ``develop`` into ``master``, you are declaring a new release of the software, because
``origin/master`` is always the production version of the codebase.

Since all branches have equal weight to git, these are conventions. There are two types of short-term
branches: ``feature`` and ``hotfix``.

.. note::

   A third kind of branch might be a non-critical bug fix. This is a fix which does not need to
   be immediately applied to production and can wait until the next development release cycle. The
   workflow for these fixes are effectively the same as developing a new feature so they are not
   given any special status in this workflow documentation. When reading the workflow for the
   feature branch development, keep in mind the same workflow applied for non-critical bug fixes.


New Feature Branches
--------------------

To create a new feature, first check the Issues section of the GitHub repository. Feature development
is driven by specific requests or problems. We like to capture these and design against them, even if
it is on the spot before diving into code. So check the issue or create a new one if there is not yet
an issue that addresses the feature.

Feature branches should always derive from ``develop``.  ``develop`` is the stable version of the
new code, and you must ensure that your feature will play nice with the current development state.
In git, you can create a branch, switch to it, and pick its parent branch all at once with the command::

    $ git checkout -b myfeature develop

It is a good habit to branch this way, because developers often forget to checkout the branches they
just created, and also may forget where they were before they cut a new branch. Both of these human
errors might cause merge headaches later.  You are allowed to create a feature branch from another
feature branch instead of ``develop``, if you are comfortable with the parent branch and have a reason
to branch from it.  However, all feature branches must eventually merge back into ``develop`` or deleted.

It's recommended practice to prefix the branch name with the issue number which it addresses. For example::

    $ git checkout -b 42-my-new-feature develop

Now that your branch is created, develop against it. Make as many commits as you'd like, and even
as many pushes to origin as you'd like.  For example::

    $ git add .
    $ git commit -m "refactored models to address issue #42"
    $ git push origin 42-my-new-feature -u

Commit messages should be descriptive. Where practical, note changed files, why you changed them, and
other metadata (WIP, not yet tested, addresses issue #42, etc.)


Pull Requests
-------------

When you are certain of the following:

- The branch has addressed the issue
- All tests pass
- Test coverage is above 80% for the entire repository
- All code is PEP8 compliant
- All migrations created if needed
- All print/debug statements removed
- The server runs as expected

then you can do a final push and create a pull request.  GitHub makes this simple. There is a
green button that reads "Review and create pull request."  You should look over the diff of the code
and make sure it reads as you intend.  If so, add a comment to the pull request that it addresses issue #42.

It is then incumbent on another member of the team to do the following:

- Pull your feature branch
- Run tests (this may be handled by a CI server such as TravisCI)
- Run migrations (this may be handled by a CI server such as TravisCI)
- Run their local dev server
- Verify that the feature was addressed

It is also incumbent upon the pull request reviewer to read the code diff and make comments on the code.
Github presents a blue and white plus icon for adding line comments.

When the reviewer agrees that the pull request is adequate, they should add a comment to the pull request.
For fun, we typically add random emoticons such as ``:frog:``.

By convention, the developer of the branch then merges it back into ``develop``, but other developers can do this step::

    $ git checkout develop
    $ git merge --no-ff 42-my-new-feature

Note that GitHub allows you to merge and delete a branch from within the Pull Request GUI.

.. note::

    The use of the ``--no-ff`` flag is not explicitly required. This flag ensures that the merge commit
    is created when merging the branch. Having a single merge commit makes it easier to rollback
    the entire branch of changes if needed. This alse has the advantage of preserving the branch information
    in the merge commit message which would otherwise be lost when the branch is deleted and
    replicates the merge behavior if the PR is merged in the Github UI. However, some projects might
    prefer to keep a cleaner history by excluding the merge commits. That is ok as well as the developers
    are in agreement and understand the trade-offs.

Branch Lifespans
-----------------

Recall that ``origin/develop`` and ``origin/master`` are the only long term branches. Every other
branch should be as short-lived as possible while still accomplishing its purpose. Dead branches
(exploratory, or failed attempts to address an issue), or feature branches that drag on a long time,
cloud the picture for other developers. Since this feature branch is no longer needed, it can be deleted
via the "delete this branch" button on GitHub, or via the command line::

    # Delete the remote branch
    $ git push origin :42-my-new-feature
    # Delete the local branch
    $ git branch -d 42-my-new-feature


Hotfix Branches
---------------

A hotfix branch is an emergency branch mandated by a critical bug or security flaw in the production
release. Hotfix branches always derive from ``origin/master``, and eventually merge back into
``develop`` and ``master``::

    $ git checkout -b hotfix-2.0.1 master
    # do the work neccessary to bump version numbers
    $ git commit -a -m "Bumped version number to 2.0.1"

When the patch or bug fix has been applied to the code, you are ready to put it into ``master``::

    $ git commit -m "Fixed severe production problem"
    $ git checkout master
    $ git merge --no-ff hotfix-2.0.1
    $ git tag -a 2.0.1
    $ git checkout develop
    $ git merge --no-ff hotfix-2.0.1
    $ git branch -d hotfix-2.0.1

.. note::

    As previously noted the ``--no-ff`` flag is not required but is recommended. See the previous
    note for more information on the advantages of using this flag.


Production Releases
-------------------

When a new production release is ready to be deployed, the latest work from ``develop`` is advanced
to the ``master`` branch. It is recommended that releases are tagged. Tags might denote the version
number for the release or the date of the release. Prior to tagging you ensure that all changes on
master are included in develop::

    $ git checkout master
    $ git pull origin master
    $ git checkout develop
    $ git pull origin develop
    $ git merge master

This merge should be a no-op. If there are changes which were not previously merged to develop you need
to ensure that develop is still running as expected before preceeding. While on the ``develop`` branch
you should 

- Update change log with release notes
- Update internal version numbers if tracked in the code
- Run test suite

Changes between each release should be noted in an obvious place in the repository such
as a ``CHANGELOG`` or ``CHANGES`` file stored at the root or a ``docs/changes.rst`` or ``docs/releases.rst``
file if there is a larger collection of documenation for the project.
The format of this file is flexible. You may look at https://github.com/caktus/margarita/blob/develop/CHANGES.rst
as an example. This uses headers to denote each released version along with the date it was released. Below the header
is a bulletted list of items which were changed/added in the release. Ideally these would also reference
the issue numbers along with these items.::

    Release Notes

    v1.0 - Aug 28, 2015
    -------------------

    - Added a great new feature (#12)
    - Fixed an annoying bug (#11)

It is not recommended to use any tool to automatically generate the change log from the git history. This file
should be written by a human to be read by a human and should add additional context otherwise not already
available in the git history.

With these changes in place you should commit the release note changes and version changes and tag the release.::

    $ git add <related files for change log and version numbers>
    $ git commit -m "Note and version bump for release <version>"
    $ git tag <version>
    $ git checkout master
    $ git merge develop
    $ git push origin master --tags
    $ git checkout develop
    $ git push origin develop --tags

With the changes and tags pushed to the central repository, you can proceed with the production deployment.
