Github
======

Every project needs a source code repository and we usually use Github to host ours. This assumes
that you'll be creating the repo in the Caktus organization, but the process is the same for any
other organization... you'll just need the permissions to do so.

#. Once you have your project set up locally, initialize your git repository and commit your files:

   .. code-block:: bash

      ~/myproject$ git init
      ~/myproject$ git commit -m "Initial project setup"

#. You'll need a Github account and your account must have been added to the `Developers
   <https://github.com/orgs/caktus/teams/developers>`_ team in the Caktus organization. Ask another
   developer, or create a `support request
   <https://caktus.atlassian.net/servicedesk/customer/portal/3>`_ to accomplish that.

#. `Create a new repo <https://github.com/organizations/caktus/repositories/new>`_. This will walk
   you through creating a repo.

   A. Leave the 'Initialize this repository with a README' checkbox **unchecked**, as you'll most likely
      be importing a repo.

   #. Don't worry about the .gitignore and LICENSE dropdowns. Our project template has its own
      .gitignore and while it's convenient to add a LICENSE here, it would be easier to just add
      that to your existing repo.

#. Click the 'Create repo' button, which will take you to a page with various instructions depending
   on your situation. We'll use the second set of instructions, labelled, '...or push an existing
   repository from the command line'. Replace ``myproject`` with the name of your newly created
   project.

   .. code-block:: bash

      ~/myproject$ git remote add origin https://github.com/caktus/myproject.git
      ~/myproject$ git push -u origin master

#. Review the 'Settings' tab to configure the repository to your preferences:

   A. Manage outside collaborators.
   #. Link Github to other services (such as HipChat, Travis CI, etc.)
   #. Manage branches. You can set the default branch to 'develop' and enable branch protection
      which can prevent force pushes to certain branches, or require Travis CI to run successfully
      on a PR before it gets merged, for example.

Private Repos
-------------

If you created a private repo, you'll need to make sure that your deployment servers are allowed to
check out your code. Once your staging server is up and running, follow `our instructions for
setting up the deploy key
<https://github.com/caktus/django-project-template/blob/master/docs/provisioning.rst#github-deploy-keys>`_.
