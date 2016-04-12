Deploying Django projects
=========================

In this section, we talk about two things:

1. The typical architecture of deployed sites
2. The interface between our deploy system and our project code -
   what the code in our projects and our deploy system expect
   from each other.

Our deploy system follows many (but not all) of the principles of
`the Twelve-Factor App <http://12factor.net/>`_. If you
haven't come across those before, I suggest you take a look,
think through the implications, then come back here.

.. toctree::
   :maxdepth: 2

   deployed-systems
   system-deploy-interface
