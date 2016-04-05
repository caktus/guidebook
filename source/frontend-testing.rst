Front-end Testing Practices
###########################

This documentation reflects the present state of our knowledge of how to test
front-end JavaScript code.

It also reflects a series of choices that were basically arbitrary because of
the lack of anything like a standard or clear best choice (e.g. the
decision to use one test runner or assertion library over alternatives).

These choices are still being experimented with, and developers should feel
free to suggest revisions if they're found to perform poorly in practice.


Testing Libraries: Overview
###########################

Mocha
-----

`Mocha <https://mochajs.org/#features>`_ is a simple and modular test library.
Unlike `Jasmine <http://jasmine.github.io/>`_, Mocha doesn't come with an
assertion library, facilities for mocks and spies, and so on. Instead it provides
a framework for writing and executing tests and lets you choose other libraries
to meet those needs.

To create a Mocha test that will be recognized by our Gulp build process,
create a file with the extension ``.spec.js`` and place it in a ``test/`` subdir
of the project's JS dir (i.e. in ``project_name/static/js/test/``).

Tests describing some value are wrapped in a callback passed to ``describe``,
containing individual test cases created with calls to ``it``::

    describe('Something', function () {
      it('returns foo', function () {
        // assertion code goes here ...
      });

      it('does not return bar', function () {
        // assertion code goes here ...
      });
    });

``describe`` calls can be nested, allowing you to represent the hierarchical
structure of your app::

    describe('your/module', function () {
      describe('YourClass', function () {
        describe('yourMethod', function () {
          //...
        });
      });
    });

This structure can be reflected in the nesting structure of the output you get
when you run tests, with certain test reporters.

One handy feature of Mocha is its simple handling of asynchronous tests. To
test async code, just include a callback as a parameter to the callback in
your ``it()`` call and invoke that callback when the test is complete::

    describe('SomethingAsync', function () {
      it('completes the async operation asyncFoo', function (done) {
        asyncFoo(function () {
          // assertions go here ...
          done(); // the test will only pass when this line runs
        });
      });
    });

Because callbacks are ubiquitous in JavaScript apps, this easy handling of async
testing makes Mocha a very attractive test library.

Chai
----

To make assertions within our tests, we use the library `Chai <http://chaijs.com/>`_.
The main benefit of Chai is that we don't really have to choose between any of
the various assertion styles that are popular in the JS world. Chai makes them
all available::

    // "should" style
    chai.should();

    foo.should.be.a('string');
    foo.should.equal('bar');
    baz.should.have.property('qux').with.length(3);

    // "expect" style
    var expect = chai.expect;

    expect(foo).to.be.a('string');
    expect(foo).to.equal('bar');
    expect(baz).to.have.property('qux').with.length(3);

    // "assert" style
    var assert = chai.assert;

    assert.typeOf(foo, 'string');
    assert.equal(foo, 'bar');
    assert.property(baz, 'qux');
    assert.lengthOf(baz.qux, 3);

Sinon
-----

For mocks, stubs, and spies, we turn to `Sinon <http://sinonjs.org/>`_, which is
something like the standard JS library in the field.

Sinon is an extremely feature-rich library, including:

* `spies <http://sinonjs.org/docs/#spies>`_
* `stubs <http://sinonjs.org/docs/#stubs>`_
* `mocks <http://sinonjs.org/docs/#mocks>`_
* `fake XHR and servers <http://sinonjs.org/docs/#server>`_
* much, much more

Consult the Sinon docks for details on those features that meet your needs.

istanbul & isparta
------------------

For test coverage, we use the libraries `istanbul <https://www.npmjs.com/package/istanbul>`_
and `isparta <https://www.npmjs.com/package/isparta>`_.

This is handled inside our the Gulp build process included in the project template.
It will check your tests' coverage of statements, branches, functions, and lines found in
the ``app/`` subdir of the project's JS dir (i.e. in ``project_name/static/js/app/``).

You can set the desired coverage thresholds inside the ``gulpfile.js``. The
numbers here represent percentages::

    .pipe(coverageEnforcer({
      thresholds: {
        statements: 80
        , branches: 50
        , lines: 80
        , functions: 50
      }
      // ...
    }))


Testing Our Stack
#################

The following front-end tools are bundled in the project template and represents
our basic stack for future projects:

* `gulp <http://gulpjs.com/>`_, the Node-based streaming build tool
* `ECMAScript 2015 <http://es6-features.org/>`_, transpiled into JavaScript
  with `Babel <https://babeljs.io/>`_
* `React <https://facebook.github.io/react/>`_, a library covering roughly the
  "view" and "controller" aspects of a MVC-architected user interface
    * `JSX <https://facebook.github.io/react/docs/jsx-in-depth.html>`_, a JS syntax
      extension that makes it easier to create React components
* `Flux <https://facebook.github.io/flux/>`_, a library and design pattern for
  managing UI application state and building UIs in a "data flow" style
    * `Immutable.js <https://facebook.github.io/immutable-js/>`_, an immutable
      data structure library used under the hood in Flux's utilities

This section of the documentation will walk through the process of setting up
tests that take these technologies into account:

* the basics of using Gulp and Babel to write and run Mocha tests in ES2015
* special techniques and gotchas related to writing tests for React components and Flux
  applications

ES2015 Mocha Tests With Gulp and Babel
--------------------------------------

Transpiling ES2015 code is already a standard part of Caktus's front-end process.
We can take advantage of the hard work that goes into this code preprocessing
to reuse parts of the process and layer new steps in without serious difficulty.

This comes out clearly in the actual test command, handled by Gulp, which
transpiles our code using Babel behind the scenes. Our Gulp test task begins::

    gulp.task('test', function () {
        require('babel-core/register');
        // ...
    });

``babel-core/register``, when imported, causes all imports within the scope to
be run through Babel. The result is that ES2015 and JSX files used by the Mocha
test runner are preprocessed without our needing to do anything special.

This is guaranteed because our ``.babelrc`` file in the top level dir of the
project sets up Babel to transpile ES2015 and JSX::

    {
      "presets": ["es2015"],
      "plugins": ["transform-react-jsx"]
    }

This allows us to not only write and test ES2015 and JSX applications but to write
our tests themselves in ES2015 and JSX.

React Tests With jsdom
----------------------

React and the `React test utilities <https://facebook.github.io/react/docs/test-utils.html>`_
both assume that the global name ``document`` points to a DOM. This will be
available when we run our code in a browser, but when running it in Node, it
will not be. This poses difficulties for testing React components.

`jsdom <https://www.npmjs.com/package/jsdom>`_ to the rescue! jsdom is a JavaScript
implementation of the DOM API. It allows us to create a fake DOM and assign it
to ``document`` so that React and its test utilities can do their magic.

The fake DOM is made available to the Mocha test process within our Gulp build
by including it in the ``require`` option of the Mocha Gulp plugin call::

      .pipe(mocha({
        require: [
          'jsdom-global/register'
        ]
      }))

Once set up in this way, Mocha will happily run tests that include statements
like these, which require the presence of a DOM at ``document``::

    TestUtils.renderIntoDocument(<AppController />);

You should make sure to clean up your fake DOM after tests that use one by
including an ``afterEach`` call that tidies it up::

    import ReactDOM from 'react-dom';
    //...

    describe('YourTestCase', () => {
      afterEach(() => {
        ReactDOM.unmountComponentAtNode(document.body);
        document.body.innerHTML = '';
      });
     });

React Testing Tips
------------------

Here are a few gotchas and tips for writing React tests with Mocha.

Stateless Functional Components Need to be Wrapped
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

React encourages you to define your React components as plain JavaScript
functions with no side effects. These are called
`stateless functional components <https://facebook.github.io/react/docs/reusable-components.html#stateless-functions>`_.

But because stateless functions don't provide an imperative API, the React
test utilities don't know how to do certain important things with them (e.g.
locate their DOM node). They also don't have lifecycle methods, making it hard
to test certain behaviors (e.g. checking their output after a state update).

To do these things, use the ``react-functional`` library to wrap your component.
Then you can test it with the test utils as usual::

    import functional from 'react-functional';
    //...

    describe('StatelessComponent', () => {
      let WrappedComponent = functional(StatelessComponent);
      TestUtils.renderIntoDocument(<WrappedComponent />);
      // ...
     });

Avoid Race Conditions by Using Callbacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're testing whether a React component updates in some way after some state
change happens, in general you won't be able to check for the update right after
running the code that's supposed to trigger it, because that update will happen
asynchronously.

To check for changes like that, use an async test and inject the ``done`` callback
into the appropriate React component lifecycle method::

    it('updates when the store changes', (done) => {
      let old_componentDidUpdate = YourComponent.prototype.componentDidUpdate;
      YourComponent.prototype.componentDidUpdate = () => {
        // this lifecycle method will be called when the update has happened
        YourComponent.prototype.componentDidUpdate = old_componentDidUpdate;
        done();
      };

      TestUtils.renderIntoDocument(<YourComponent />);
      A.triggerStateChangeThatAffectsYourComponent();
    });

Testing Server Interactions
---------------------------

Figuring out how to mock jQuery AJAX requests is a work in progress. For now,
try to avoid using those.

Instead, try the new `Fetch API <https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API>`_.
Or, well, try a `fetch polyfill <https://github.com/github/fetch>`_.

To test these, you can use `fetch-mock <https://www.npmjs.com/package/fetch-mock>`_.
This will mock the value of ``window.fetch``, allowing you to set up fake HTTP
request results in your test setup (and restore them afterwards)::

    describe('YourStore', () => {
      beforeEach(() => {
        fetchMock
          .mock('/path/to/test_data.json', DATA)
        ;
      });

      afterEach(() => {
        fetchMock.restore();
      });
    });

Testing With Immutable Data
---------------------------

Stores created with the `Flux utilities <https://facebook.github.io/flux/docs/flux-utils.html>`_
use `Immutable.js <https://facebook.github.io/immutable-js/>`_ data structures
under the hood.

If you want to test data stores created with the Flux utils, you'll have to import
from ``immutable`` and use the immutable.js data types' APIs appropriately.

Here, for example, you can use the ``count`` method of immutable collections to
count the number of key-value pairs in the immutable Map returned from this Store::

    it('has three items on inspection', () => {
      let items = YourStore.getState();
      assert.equal(3, items.count());
    });

See the `Immutable.js docs <https://facebook.github.io/immutable-js/docs/>`_ for
more info on how to work with key types like Map, Seq, and Collection.
