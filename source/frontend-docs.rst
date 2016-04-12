Front-end documentation with JSDoc
##################################

Writing maintainable and understandable front-end JavaScript code calls for writing
particularly thorough documentation. JavaScript is an unusually flexible language in which
protocols and expectations are rarely if ever obvious without carefully reading
the code. It's also a language with a huge and diverse set of libraries where
standards and conventions are in a constant state of flux. The only way to
ensure that the developer who inherits your front-end code tomorrow or a year
from now will understand what your program does is to carefully document your code,
more so than you may be accustomed to doing on Python and other non-JS projects.

A good way to document your JS is by using `JSDoc <http://usejsdoc.org/>`_ and its
commenting conventions. JSDoc is an API documentation generator that can be used
to generate a complete documentation site from comments in your JS code. The
comment syntax associated with JSDoc, derived from that of JavaDoc, is also widely
used in major JS projects. Whether or not you use JSDoc to generate an API
docs site for your code, following the JSDoc conventions is a good way to ensure
that your comments are as informative and immediately comprehensible as possible.

JSDoc installation and basic setup
==================================

JSDoc can be added to an existing project as an npm dependency. To take advantage
of JSDoc 3.4's native support for ECMAScript 2015, install JSDoc version
3.4.0 or later::

    npm install jsdoc^3.4.0 --save-dev

For most projects, you will want to create a configuration file that will
tell JSDoc such things as which files to ignore, which plugins to use, etc.
Full instructions can be found `on the JSDoc site <http://usejsdoc.org/about-configuring-jsdoc.html>`_.

Our recommended practice is to call the configuration file ``.jsdoc.json`` and to place it in your root
project directory (alongside other config files like ``.gitignore``, ``.babelrc``, etc).
This configuration file specifies the plugins JSDoc will use, among other things.

In your config file, you can set up the source directories
that JSDoc will look through as it crawls your JS code, as well as the output
directory into which it will place the documentation site it builds.
In projects created with our project template, the source dir will look
like ``project_name/static/js``; we recommend ``docs/js`` as the dir for docs output.

Caveats:

* You'll also want to enable the ``recurse`` option so that your entire source tree
will be scanned.
* If your site's JavaScript build output is located in the same directory
as its source, you will also want to throw in an ``excludePattern`` so that only
source JS is crawled.

Following our recommendations gives you a config file like::

    {
      "source": {
        "excludePattern": "bundle\\.js",
        "include": [
          "project_name/static/js"
        ]
      },
      "opts": {
        "recurse": true,
        "destination": "docs/js"
      }
    }

If your project is based off the Caktus project template, it probably uses
React as well as the JSX component-specification DSL; and it probably also
uses Babel to preprocess both. Because JSDoc can use your existing Babel
setup, it takes very little additional work to ensure that JSDoc can read
your code. You will need the ``jsdoc-babel`` plugin::

    npm install --save-dev jsdoc-babel

And you will need to add lines to your config file to add the plugin and to
get JSDoc to recognize ``.jsx`` files as well as ``.js`` ones::

    {
      "plugins": ["node_modules/jsdoc-babel"],
      "source": {
        "includePattern": ".+\\.jsx?$",
        /* ... */
      },
      /* ... */
    }

That's it. Assuming Babel is correctly configured to process your JSX code,
JSDoc will now be able to handle it, too.

Once the configuration file is set up, you can generate a JSDoc site from your
JS by running this command (assuming ``./node_modules/.bin`` is in your
``$PATH``)::

    jsdoc -c .jsdoc.json

That's it! Your JSDoc documentation will have been deposited in ``./docs/js``.

JSDoc is not a library and doesn't expose a full-featured API. For that
reason, to use JSDoc from within your build process, it should be treated as
just another command line program to be run using Node's ``child_process``.

JSDoc: suggested comment style
==============================

JSDoc offers a very rich selection of tags and other features and a great deal
of flexibility in how it can be used. We recommend adhering to at least these
conventions:

* Create a doc comment for every module, class, function / method, and event.
* For every function / method doc comment, include:
    * A prose description of the function's purpose
    * ``@param`` tags for each expected parameter, including:
        * name
        * type
        * prose description
    * For Object-type parameters, include separate ``@param`` entries for each
      property expected on the Object
    * ``@returns`` tag giving the function's return value, including:
        * type
        * prose description
        * separate ``@param`` entries for expected properties on returned Objects
    * ``@fires`` tags indicating events fired within the function body
* If a function is a callback:
    * Declare its doc comment with ``@callback``
    * Specify the event(s) it's attached to with ``@listens``
* Include ``@see`` references wherever another part of the code provides useful
  context for interpreting the comment.

For the full details of what JSDoc is capable of, see `the JSDoc website <http://usejsdoc.org/>`_.

Additional Usage
================

Comment style
-------------

An ES6 module can be documented by adding a JSDoc comment with the
``@module`` tag with the identifier for the module (e.g. ``@module foo/bar``
for a module loaded with ``import * as fooBar from 'foo/bar'``)::

    /** @module foo/bar */

An ES6 class can be documented by adding a JSDoc comment to its
constructor. Note that while this JSDoc comment is applied to the constructor
method, it will be treated as documentation for the class itself and listed
in the doc index as such.

The class documentation comment includes a brief prose description of
the class's nature; it explicitly identifies the function as a
constructor using ``@constructs``; it spells out the type of its single
required parameter, ``options``, and the attribute ``id`` that it
requires; and it uses ``@see`` to link to the docs for the method
``appSetup`` which does the constructor's heavy lifting::

    export default class ShowMatches extends Model {
      /**
       * The app state model.
       *
       * @constructs ShowMatches
       * @param {Object} options - initialization options for app.
       * @param {string} options.id - ID of dataset.
       *
       * @see ShowMatches#appSetup
       */
      constructor (options, ...rest) {
        super(options, ...rest);
        this.__options__ = options;
        this.appSetup(options);
      }

      // ...
    }

This example of a JSDoc comment for a method on this class contains
a prose description indicating how it fits in with the flow of the
app; it specifies the type of its single parameter by linking to
the docs for a class defined in a separate module, also indicating
with the ``Type[]`` notation that the argument is an array of values
of that type; it indicates via ``@fires`` that calling the function
fires an event, and it links to the docs for that event; and it
uses ``@see`` to accompany the reference to ``PossibleMatches`` with
an explicit link to its documentation::

    /**
     * Method called to compare a collection of potential matches, triggered
     * by the PossibleMatches view.
     *
     * @method ShowMatches#compareMatches
     * @param {module:models/PossibleMatch.PossibleMatch[]} matches - set of
     *     matches to compare
     * @fires ShowMatches#event:change:comparing_matches
     * @see module:views/PossibleMatches
     */
    compareMatches (models) {
      this.set('comparing_matches', new PossibleMatchesCollection(models));
    }

.. caution:: Note that ``@method`` gives the name of the class and the
method. If you don't do this and just say ``@method`` (which the JSDoc docs
say you can do), assuming your method is an ECMAScript 2015 class method,
JSDoc will not generate documentation for your method.

A callback for an event can be documented like this. This doc comment
indicates that the function is to be used as a callback by declaring
it with ``@callback``. It specifies the event it listens for using ``@listens``.
Finally, since executing the callback also triggers an event, it
specifies that event with ``@fires``::

    /**
     * Handles the changing of the set of potential matches being compared.
     *
     * @callback ShowMatches#changeComparingMatches
     * @listens ShowMatches#event:change:comparing_matches
     * @fires ShowMatches#event:change:active_master_view
     */
    changeComparingMatches () {
      this.set('active_master_view', 'possible-matches-detail');
    }

Custom or otherwise app-relevant events can be documented in
free-standing JSDoc comment blocks. This event doc comment indicates
the name of the event with ``@event``, and it documents each parameter
passed to its event listeners with ``@param`` (i.e. the callback for
``change:new_id`` should take two arguments, ``app`` and ``new_id_p``,
whose types and significance are spelled out here)::

    /**
     * Event representing the process of assigning a new ID to the current
     * active Person record.
     *
     * @event ShowMatches#event:change:new_id
     * @param {ShowMatches} app - the changing app
     * @param {Promise} new_id_p - promise representing the HTTP request to
     *     assign a new ID to the current active Person
     */
