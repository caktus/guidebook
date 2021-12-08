Frontend Packaging
==================

Caktus has adopted frontend packaging standards to make management of
dependencies in frontend development as robust as they are in backend
development. Javascript dependencies are configured and installed via a
standard `package.json` configuration for each project and the NPM tool
as part of NodeJS 4.2 or newer. The tool Browserify is used to collect
and combine all of a project\'s imported modules into a single bundle.

Projects created with the Caktus Django Project Template after January
8th, 2016 will come pre-configured with this setup. Older projects would
need to upgrade to Margarita 1.4.0 or newer and follow the [Frontend
Packaging Upgrade Guide](#frontend-packaging-upgrade-guide) below in
order to use this setup.

Frontend Packaging Upgrade Guide
--------------------------------

If you\'re on a project created before January 8th, 2016 you\'ll need to
upgrade both your project and its version of
[Margarita](https://github.com/caktusgroup/margarita) in order to use
these frontend packaging techniques.

Upgrading to Margarita 1.4.0 will require adding a few files to the
project, which configure it as a NodeJS package for the purposes of
defining dependencies and build instructions for the frontend
components.

First, you will need a Gulpfile, which is our frontend version of the
Fabfile. Second, you\'ll need a `package.json` file defining the project
for NPM, and defining the initial set of package dependencies.

You can download and add these from this documentation:

-   [gulpfile.js](_static/files/gulpfile.js)
-   [package.json](_static/files/package.json)

and add them to the top level of your project. You\'ll need to modify
both with the correct project name.

Now, you can add these extra lines to your `.gitignore`:

    node_modules
    */static/js/bundle.js
    */static/css

You probably have existing Javascript and stylesheets to move into the
new build system. The next sections will cover each of these.

### Migrating Existing Setup

You\'ll have several pieces of the old setup to migrate to the new
setup.

#### Django Compressor

Because we no longer use Django Compressor to process frontend assets,
you can remove the dependency from `requirements/base.txt` and your
settings `base.py` module. If you have this `STATICFILES_FINDERS`:

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    )

Then you can safely remove the entire setting and leave the defaults. If
your project has defined any other finders, then only remove the one
from `compressor`.

Remove it also from `INSTALLED_APPS` and remove `COMPRESS_PRECOMPILERS`.
Check your settings for any other place to remove references to it.

You\'ll need to remove compressor from the `base.html` where it is used
to include both Javascript and Less stylesheets. Remove the
`{% load compressor %}` line at the top of the template. We\'ll change
the compressor tags for the Javascript first, which should currently
look like this:

    {% compress js %}
        <script src="{% static 'js/site.js' %}"></script>
    {% endcompress %}

but, this may include more than one script tag. If it does, you\'ll need
to follow the section on [Existing Javascript]{.title-ref} to migrate
them to a bundle. This line will be replaced with one tag loading our
combined bundle of all project Javascript:

    <script src="{% static 'js/bundle.js' %}"></script>

The section using compressor to compile Less stylesheets will also be
replaced, from this:

    {% if debug %}
        <link rel="stylesheet/less" type="text/css" media="all" href="{% static 'less/site.less' %}">
        <script src="//cdnjs.cloudflare.com/ajax/libs/less.js/1.5.1/less.min.js"></script>
    {% else %}
        {% compress css %}
            <link rel="stylesheet" type="text/less" media="all" href="{% static 'less/site.less' %}">
        {% endcompress %}
    {% endif %}

to this:

    <link rel="stylesheet" media="all" href="{% static 'css/bundle.css' %}">

#### Existing javascript

If you have a frontend-light project that has only a single JS file,
rename it to `static/js/index.js` in the project. If you have multiple
scripts, you\'ll need to create this file and import the different
scripts in your project. (Read the section below on [Using Frontend
Packages]{.title-ref})

#### Existing Stylesheets

If you have a single stylesheet you\'ll need to rename it
`less/index.less` and if you have multiple you\'ll need to create this
single stylesheet and, within it, import other stylesheets like

``` {.sourceCode .less}
@import "./states.less";
@import "./base.less";
@import "./header.less";
```

Stylesheets might be distributed by NPM, either on their own or as part
of a widget library. For example, bootstrap can be installed by NPM
giving us both the interactive implementation of its widgets and also
the bootstrap Less files. If you\'ve installed a package with
stylesheets from NPM, you can import those stylesheets in your
`index.less` like so:

``` {.sourceCode .less}
@import (less) "node_modules/bootstrap/less/bootstrap.less";
```

or even plain CSS stylesheets

``` {.sourceCode .less}
@import (css) "node_modules/foo-widget/css/foo-widget.css";
```

Each package might put the Less or CSS stylesheets in different
locations under the path `node_modules/PACKAGE/`. Find the stylesheet
you need and its location to determine the proper path.

#### Modernizr

Your project likely includes a copy of Modernizr, but the new frontend
setup builds a recent copy of this (and is configurable), so we can
change this line:

    <script src="//cdnjs.cloudflare.com/ajax/libs/modernizr/2.7.1/modernizr.dev.js"></script>

to this:

    <script src="{% static 'libs/modernizr.js' %}"></script>

#### jQuery

If you need the jQuery library accessible for script tags that might be
in specific pages and won\'t be pulled in by the bundling process, then
it might be prudent to keep the jquery library included by the existing
`<script>` tag, and that\'s okay for now. You can move this JS out of
the template in a future improvement.

If you do not need this and only use jQuery within code you\'re already
moving into modules, then jQuery can be a dependency imported by the new
system. If you want to do this, remove the jQuery `<script>` tag and
then install jQuery (whatever version is appropriate for you):

    npm install --save-dev jquery@2.2.0

If you need jQuery to be globally available, you can add this line to
the top of your `index.js` under the imports:

    window.jQuery = window.$ = require('jquery')

Any modules which use jQuery *should* avoid the global and import the
library within that module.

``` {.sourceCode .javascript}
import 'jQuery';

jQuery.fn.plugin = function() {
    ...
}
```

Using Frontend Packages
-----------------------

Our frontend packaging includes configuration to support the newest
version of the Javascript language ES2015, which includes many updates
including proper module support and an import statement. To use packages
installed in your project you can import the default export from the
project under a name of your choosing:

    import $ from 'jquery';

For some packages, you\'ll likely want to import more than one thing
from it:

    import { AutoBind, jQueryClass } from './helpers/jquery';

### Organizing Project Frontend Code

Packages aren\'t just for the third party code you depend on. You\'ll
benefit from organizing your project\'s own Javascript the same way.
This setup begins with a top-level module in your project at
`static/js/index.js`. This module is only expected to be an initial
point to import all your dependencies and do very basic initialization.

A note for projects that use jQuery: because of the global nature of
jQuery and the hoisting nature of ES2015 import statements, it can be
very difficult to import jQuery in a way that makes it easily available
to other scripts, such as plugins. We have found a double import method
as follows works around these issues:

``` {.sourceCode .javascript}
import $ from 'jquery'
/* ... additional imports ... */

window.jQuery = window.$ = require('jquery')
```

The first, native import will ensure jQuery is loaded early as a
dependency. The second version uses the non-native `require()` function,
which is the NodeJS format for module import before ES2015. This version
is just a regular line of code and so it will *not* be hoisted and can
properly inject the window globals `jQuery` and `$`.

### Creating And Using Modules

New functionality may require you organize it into its own module. Use
your best judgement here, but consider the same sort of reasoning we use
to draw lines between functionality in Python. You can also group
related modules into a package, by placing them in a directory.

You can import your module to load it from the `index.js`

``` {.sourceCode .javascript}
import './utils.js'
```

The `./` is necessary to distinguish from modules that would be loaded
from the standard library or NPM installed packages. These imports are
simply relative paths to the location of the module.

You only need to include modules you might consider \"top-level\" in
`index.js`. For example, if you defined a helper function
`get_csrf_token()` in that `utils.js` and only needed to use that one
function in another module, you would import it there,

``` {.sourceCode .javascript}
import get_csrf_token from 'utils.js';
```

This would assume that, in `utils.js`, the function had been exported.

``` {.sourceCode .javascript}
export function get_csrf_token() {
    ...
}
```

Installing New Packages
-----------------------

When adding new frontend dependencies you should find an NPM packaged
distribution of the version you need. Preferably the vendor or project
will manage this, but the Javascript world is still catching up to
proper packaging and you may find third-party distributions which are
also acceptable.

You can install an NPM package both locally and configured in your
package.json with a single command:

    npm install --save package-name==1.2.3

Upgrading Existing Packages
---------------------------

Periodically we need to look at upgrading the versions of third-party
packages we depend on. This includes multiple steps.

-   Identify new versions of packages we use.
-   Upgrade to a newer version of a package and successfully test that
    no regressions occur.
-   Update `package.json` with the new version and commit this change.

We can make this process a little easier, and we can also enforce some
rules about them thanks to NPMs. When specifying package versions in
`package.json` we can tell NPM about how we want it to interpret the
version number we give.

Version strings have the form \"major.minor.patch\". Parts can be
omitted starting from the right, e.g. \"1.2\" is major 1, minor 2; and
\"1\" is major 1.

-   Including `x` or `*` in the version string allows that part of the
    version to be increased. E.g. `1.2.x` allows versions `>= 1.2.0` and
    `< 1.3.0`.

There are some commonly used shorthand prefixes, `~` and `^`. These
always mean at least the version as written, plus possibly newer
versions, as follows.

-   Prefixing a version with `~` allows changes in the patch-level if
    the specified version includes a minor version, or in the minor
    version if only a major version is specified. E.g. `~1.2.0` means
    the same as `1.2.*` or `1.2.x`, `~1.2.3` means `>= 1.2.3` and
    `< 1.3.0`, and `~1.2` means `>= 1.2.0` and `< 1.3.0`, and `~1` would
    mean `>= 1.0.0 and <1.1.0`.
-   Prefixing a version with `^` allows changes that do not modify the
    left-most non-zero digit in the version. So `` ^0.2.3` means ``\>=
    0.2.3`and`\< 0.3`.  But`\^0.0.3`means exactly`0.0.3\`\`.

We document these because they are very widely used and even inserted
into `package.json` by the tools, but if you prefer when writing version
specifications yourself, you can write them in the obvious more verbose
way, e.g. `>=1.2.3 <2.4.0`.

You may have NPM update all packages to the latest versions within their
constraints at any time:

    npm update

And this is run on all deploys after `npm install` to update previously
installed packages.

Updating Your Project Setup
---------------------------

When pulling changes in a project down to your local development
environment, you\'ll need to update both backend and frontend packages:

> make update
