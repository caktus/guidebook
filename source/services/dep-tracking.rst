Dependency Tracking
###################

Projects rely heavily on often a large number of third-party packages, and those
packages hopefully continue to receive updates, bug fixes, optimizations, and
new features. We want to be aware of those updates when they are available,
especially when new available updates include security fixes that would be
particularly important for us to update in our projects.

Requires.io
===========

Our Python dependencies can be tracked with the requires.io tool.

There are two modes to integrate with, depending on if you're using a public repository or a
private one. If you're using a public repository, you can log into requires.io using your GitHub
account.

You'll be presented with a list of available public repositories to navigate for all of your
repositories. Navigate to your new project and click the "Activate" button. On the project details
page choose the branch you'd like to show requirements for, preferably the master branch. You'll
see a report of dependencies for this branch.

At the top of the page you'll see a requirements badge with a link "Show badge urls" which will
expand to give you snippets you can add to the top of the project's README to show this badge
on the github project page.



BitBound
========

Our Javascript dependencies can be tracked with BitBound.

To setup a new project with BitBound, first `log into service <https://www.bithound.io/>`__ with
your Caktus GitHub account. Navigate to your list of repositories by clicking on your avatar in
the upper right corner and clicking on "Repositories". Click the button labeled "Add Projects",
which will take you to a list of all organizations you have access to and their repositories.

Select the appropriate organization first and then enter the name of the repository in the filter
box. Click "Add Project".

You'll be taken to the project Dashboard, where you'll see an analysis of the project running.
This step might take some time to complete, depending on work load and the size of the project.

When the analysis is complete go to the "Dependencies" section and you'll find a report of all NPM
dependencies in the project. Snippets to add a badge reporting the current analysis of the project
can be found on the right hand side. Copy and paste the appropriate snippet into the project's
README file at the top, preferably beside the badge from the Requires.io service.
