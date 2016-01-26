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

JSDoc can be added to an existing project as an npm dependency::

    npm install jsdoc --save-dev

For most projects, you will want to create a configuration file that will
tell JSDoc such things as which files to ignore, which plugins to use, etc.
Full instructions can be found `on the JSDoc site <http://usejsdoc.org/about-configuring-jsdoc.html>`_.

Once the configuration file is set up, you can generate a JSDoc site from your
JS by running this command::

    node ./node_modules/jsdoc/jsdoc.js -c name-of-config-file.json -r path/to/js -d output/dir

If your project uses ECMAScript 2015 with Babel, you need to use
the ``jsdoc-babel`` plugin::

    npm install jsdoc@3.3.x jsdoc-babel --save-dev

You will then need to set up your configuration file to include ``jsdoc-babel``::

    {
      "plugins": ["node_modules/jsdoc-babel"]
    }

Assuming Babel is configured properly (i.e. that you have a valid .babelrc
file tailored to your project's needs), JSDoc should "just work" after the
Babel plugin is included.

JSDoc is not a library and doesn't expose a full-featured API. For that
reason, to use JSDoc from within your build process, it should be treated as
just another command line program to be run.

In Gulp, for instance, you can run the above command by means of Node's
``child_process``, like so::

    gulp.task('jsdoc', function (cb) {
      child_exec('node ./node_modules/jsdoc/jsdoc.js -c ./name-of-config-file.json -r ./path/to/js -d ./output/dir', undefined, cb);
    });

JSDoc: suggested comment style
==============================

JSDoc offers a very rich selection of tags and other features and a great deal
of flexibility in how it can be used. We recommend adhering to at least these
conventions:

* Create a doc comment for every module, class, function / method, and event.
* For every function / method doc comment, include:
    * A prose description of the function's purpose
    * ``@param`` tags each expected parameter, including:
        * name
        * type
        * prose description
    * For Object-type parameters, include separate ``@param`` entries for each
      property expected on the Object
    * ``@returns`` tag giving the function's return value, including:
        * type
        * prose description
    * ``@fires`` tags indicating events fired within the function body
* If a function is a callback:
    * Declare its doc comment with ``@callback``
    * Specify the event(s) it's attached to with ``@listens``
* Include ``@see`` references wherever another part of the code provides useful
  context for interpreting the comment.

For the full details of what JSDoc is capable of, see `the JSDoc website <http://usejsdoc.org/>`_.

Examples
========

Basic configuration file
------------------------

For an ES6-enabled project using JSX syntax for React components and
Babel transpilation, a minimal JSDoc configuration file would look
like this::

    {
      "plugins": ["node_modules/jsdoc-babel"],
      "source": {
        "includePattern": ".+\\.jsx?(doc)?$"
      }
    }

The corresponding ``.babelrc`` file would look like this::

    {
      "presets": ["es2015"],
      "plugins": [
        "syntax-jsx",
        "transform-react-jsx"
      ]
    }

Assuming the configuration file is called ``conf.json``, the app's
code lives in the directory ``./app``, and the desired output directory
is ``./out``, JSDoc can be called like so::

    node ./node_modules/jsdoc/jsdoc.js -r ./app -c ./conf.json -d ./out

Comment style
-------------

An ES6 module can be documented by adding a JSDoc comment to its
constructor. This comment includes a brief prose description of
the class's nature; it explicitly identifies the function as a
constructor using ``@constructs``; it spells out the type of its single
required parameter, ``options``, and the attribute ``id`` that it
requires; and it uses ``@see`` to link to the docs for the method
``appSetup`` which does the constructor's heavy lifting::

    export default class ShowMatches extends Model {
      /**
       * Create a new app state model.
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
