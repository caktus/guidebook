Dependency Tracking
===================

Projects often rely heavily on a large number of third-party packages,
and those packages hopefully continue to receive updates, bug fixes,
optimizations, and new features. We want to be aware of those updates
when they are available, especially when new available updates include
security fixes that would be particularly important for us to update in
our projects.

Requires.io
-----------

Our Python dependencies can be tracked with the requires.io tool.

You\'ll need to register for an API account at <https://requires.io/>
and pass a request to the sysadmin team to add the new username to our
enterprise Requires.io account.

To add your project to requires.io you\'ll need to register it, and you
can find [instructions and an authentication
token](https://requires.io/enterprise/Caktus/api/) for the Caktus
account.

1.  Copy the token found under the Token header and copy it in the
    Travis CI settings for the project as an environment variable named
    `REQUIRES_IO_TOKEN`.
2.  Add the requirement `requires.io` to `requirements/dev.txt`.
3.  Run `pip install -U -r requirements/dev.txt` to install the tool
4.  Set the Caktus token in your local `.env`:

        echo "REQUIRES_IO_TOKEN=<Token from API page>" >> .env
        source .env

5.  Register the new repository with the Caktus token:

        requires.io update-repo -t $REQUIRES_IO_TOKEN \
          -r <PROJECT_NAME> --private

BitHound
--------

Our Javascript dependencies can be tracked with BitHound.

To setup a new project with BitHound, first [log into
service](https://www.bithound.io/) with your Caktus GitHub account.
Navigate to your list of repositories by clicking on your avatar in the
upper right corner and clicking on \"Repositories\". Click the button
labeled \"Add Projects\", which will take you to a list of all
organizations you have access to and their repositories.

Select the appropriate organization first and then enter the name of the
repository in the filter box. Click \"Add Project\".

You\'ll be taken to the project Dashboard, where you\'ll see an analysis
of the project running. This step might take some time to complete,
depending on work load and the size of the project.

When the analysis is complete go to the \"Dependencies\" section and
you\'ll find a report of all NPM dependencies in the project. Snippets
to add a badge reporting the current analysis of the project can be
found on the right hand side. Copy and paste the appropriate snippet
into the project\'s README file at the top, preferably beside the badge
from the Requires.io service.

GitHub Project Badges
---------------------

To make monitoring the current state of projects easier we can embed a
set of badges from third party services. The following template will
include badges for Travis CI, Requires.io, and BitHound.

``` {.sourceCode .rst}
+-----------------+------------------------+------------------------+
|                 | Develop                | Master                 |
+=================+========================+========================+
| Travis CI       | |badge-travis-develop| | |badge-travis-master|  |
+-----------------+------------------------+------------------------+
| Python Deps     | |badge-reqsio-develop| | |badge-reqsio-master|  |
+-----------------+------------------------+------------------------+
| Javascript Deps | |badge-bithnd-develop| |                        |
+-----------------+------------------------+------------------------+

.. |badge-travis-develop| image:: https://magnum.travis-ci.com/ORGANIZATION/REPOSITORY.svg?token=TRAVIS_CI_TOKEN&branch=develop
    :target: https://magnum.travis-ci.com/ORGANIZATION/REPOSITORY

.. |badge-reqsio-develop| image:: https://requires.io/enterprise/Caktus/REPOSITORY/requirements.svg?branch=develop
    :target: https://requires.io/enterprise/Caktus/REPOSITORY/requirements/?branch=develop

.. |badge-bithnd-develop| image:: BITHOUND_BADGE_IMAGE_URL
    :target: https://www.bithound.io/github/ORGANIZATION/REPOSITORY/develop/dependencies/npm

.. |badge-travis-master| image:: https://magnum.travis-ci.com/ORGANIZATION/REPOSITORY.svg?token=TRAVIS_CI_TOKEN&branch=master
    :target: https://magnum.travis-ci.com/ORGANIZATION/REPOSITORY

.. |badge-reqsio-master| image:: https://requires.io/enterprise/Caktus/REPOSITORY/requirements.svg?branch=master
    :target: https://requires.io/enterprise/Caktus/REPOSITORY/requirements/?branch=master
```
