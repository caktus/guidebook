Frontend Packaging
##################

Caktus has adopted frontend packaging standards to make management of
dependencies in frontend development as robust as they are in backend
development. Javascript dependencies are configured and installed via
a standard `package.json` configuration for each project and the NPM
tool as part of NodeJS 4.2 or newer. The tool Browserify is used to
collect and combine all of a project's imported modules into a single
bundle.

Projects created with the Caktus Django Project Template after January
8th, 2015 will come pre-configured with this setup. Older projects
would need to upgrade to Margarita 1.4.0 or newer and follow the
`Frontend Packaging Upgrade Guide`_ below in order to use this setup.

Frontend Packaging Upgrade Guide
================================

If you're on a project created before January 8th, 2015 you'll need
to upgrade both your project and its version of
`Margarita <https://github.com/caktusgroup/margarita>`__ in order to
use these frontend packaging techniques.

Upgrading to Margarita 1.4.0 will require adding a few files to
the project, which configure it as a NodeJS package for the
purposes of defining dependencies and build instructions for the
frontend components.

First, you will need a Gulpfile, which is our frontend version of the
Fabfile. Second, you'll need a ``package.json`` file defining the project
for NPM, and defining the initial set of package dependencies.

You can download and add these from this documentation:

* `gulpfile.js </_static/files/gulpfile.js>`__

* `package.json </_static/files/package.json>`__

and add them to the top level of your project. You'll need to modify
both with the correct project name.

Finally, you can add these extra lines to your ``.gitignore``::

    node_modules
    */static/js/bundle.js
    */static/css

**TODO** Finish the upgrade section. It is incomplete.

Using Frontend Packages
=======================

Our frontend packaging includes configuration to support the newest version of
the Javascript language ES2015, which includes many updates including proper
module support and an import statement. To use packages installed in your project
you can import the default export from the project under a name of your choosing::

    import $ from 'jquery';

For some packages, you'll likely want to import more than one thing from it::

    import { AutoBind, jQueryClass } from './helpers/jquery';

Organizing Project Frontend Code
--------------------------------

Packages aren't just for the third party code you depend on. You'll
benefit from organizing your project's own Javascript the same way. This setup begins
with a top-level module in your project at ``static/js/index.js``. This module
is only expected to be an initial point to import all your dependencies and do
very basic initialization.

A note for projects that use jQuery: because of the global nature of jQuery and
the hoisting nature of ES2015 import statements, it can be very difficult to import
jQuery in a way that makes it easily available to other scripts, such as plugins.
We have found a double import method as follows works around these issues:

.. code-block:: javascript

    import $ from 'jquery'
    /* ... additional imports ... */

    window.jQuery = window.$ = require('jquery')

The first, native import will ensure jQuery is loaded early as a dependency. The second
version uses the non-native ``require()`` function, which is the NodeJS format for
module import before ES2015. This version is just a regular line of code and so it will
*not* be hoisted and can properly inject the window globals ``jQuery`` and ``$``.

Creating And Using Modules
--------------------------

New functionality may require you organize it into its own module. Use your best
judgement here, but consider the same sort of reasoning we use to draw lines between
functionality in Python. You can also group related modules into a package, by placing
them in a directory.

You can import your module to load it from the ``index.js``

.. code-block:: javascript

    import './utils.js'

The ``./`` is necessary to distinguish from modules that would be loaded from the
standard library or NPM installed packages. These imports are simply relative paths to
the location of the module.

You only need to include modules you might consider "top-level" in ``index.js``. For
example, if you defined a helper function ``get_csrf_token()`` in that ``utils.js``
and only needed to use that one function in another module, you would import it there,

.. code-block:: javascript

    import get_csrf_token from 'utils.js';

This would assume that, in ``utils.js``, the function had been exported.

.. code-block:: javascript

    export function get_csrf_token() {
        ...
    }

Installing New Packages
=======================

When adding new frontend dependencies you should find an NPM packaged distribution
of the version you need. Preferably the vendor or project will manage this, but the
Javascript world is still catching up to proper packaging and you may find third-party
distributions which are also acceptable.

You can install an NPM package both locally and configured in your package.json
with a single command::

    npm install --save package-name==1.2.3

Upgrading Existing Packages
===========================

Periodically we need to look at upgrading the versions of third-party packages we
depend on. This includes multiple steps.

* Identify new versions of packages we use.
* Upgrade to a newer version of a package and successfully test that no regressions occur.
* Update ``package.json`` with the new version and commit this change.

We can make this process a little easier, and we can also enforce some rules about them
thanks to NPMs. When specifying package versions in ``package.json`` we can tell NPM about
how we want it to interpret the version number we give.

* ``1.2`` installs the newest ``1.2`` patch release
* ``1.2.x`` or ``~1.2.3`` do the same, but the later defines the original minimum specified
  when the package version was last pinned.
* ``1`` or ``1.x`` or ``^1.2.3`` specify a minimum version, but allow any more recent *minor*
  release such as ``1.3.0`` to be installed, if it is available.

NPM dictates packages follow strict semver versioning rules, which instruct that patch
releases should only include bugfixes and minor releases can include new functionality but
must remain backwards compatible. Only major releases are allowed to break backwards
compatibility.

These rules are followed pretty well, but there are instances when a project might fail to
follow the "no breaking changes in minor releases" rule, either mistakenly or intentionally.
A package should be pinned with the ``~`` constraint if it may do this.

You may have NPM update all packages to the latest versions within their constraints at any
time::

    npm update

And this is run on all deploys after ``npm install`` to update previously installed
packages.

Updating Your Project Setup
===========================

When pulling changes in a project down to your local development environment,
you'll need to update both backend and frontend packages:

    pip install -U -r requirements/dev.txt
    npm install
    npm update
