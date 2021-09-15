Developer Machine Setup
#######################

This document includes instructions on setting up pre-requisites for this project on a new machine.

Mac OS X
========

Every developer machine is expected to include a few pre-requisites used by most or all projects.

Command Line Tools
''''''''''''''''''

Before you install anything else you'll need to install Apple's own 'Command Line Tools' package.
This includes a base set of common command line programs used by developers, but not shipped by
default in OSX. You may need to re-install this package after major upgrades to OSX.

Apple does provide a simple utility for bootstrapping these tools and installing them::

    xcode-select --install

Get more information about the Command Line Tools directly from Apple:

    https://developer.apple.com/library/ios/technotes/tn2339/_index.html#//apple_ref/doc/uid/DTS40014588-CH1-WHAT_IS_THE_COMMAND_LINE_TOOLS_PACKAGE_


Homebrew
''''''''

Homebrew is a project that provides automated download, compilation, and install of a wide range
of developer and console tools for the Mac.

A self-executing install script can be fetched and run simply, from the Homebrew documentation::

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

You can receive more information in the Homebrew documentation or see a full list of packages
available once you've installed it.

* Homebrew Docs: https://github.com/Homebrew/homebrew/tree/master/share/doc/homebrew#readme
* Package List: https://github.com/Homebrew/homebrew/tree/master/Library/Formula

OpenSSL
'''''''

There are known incompatibilies with the OpenSSL library shipped with OSX, but Homebrew gives us
a more up-to-date version to link against. We need to both install and force-link this one::

    brew install openssl

Version Control
'''''''''''''''

Install Mercurial and Git, the version control systems used by most
projects to obtain and coordinate changes to the code base between all
developers::

    brew install git
    brew install mercurial

PostgreSQL
''''''''''

The first important package to install from Homebrew is the PostgreSQL database and the PostGIS
extensions::

    brew install postgresql
    brew install postgis

With PostgreSQL installed, you'll want to make sure it runs every time your machine comes up, and
to start it running immediately::

    mkdir -p ~/Library/LaunchAgents
    cp /usr/local/Cellar/postgresql/$(postgres --version|cut -d' ' -f3)/homebrew.mxcl.postgresql.plist ~/Library/LaunchAgents/
    launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist

Python
''''''

Mac OS X installers for all the latest Python versions can be downloaded from:
https://www.python.org/downloads/mac-osx/

Practically speaking (as of February 2019, at least), it is helpful to have Python 2.7, 3.5, 3.6,
and 3.7 all installed locally (soon, probably 3.8 as well).

On the Mac OS X installer download page, find the "macOS 64-bit installer" link for the latest
point release of the Python major version that you want to install. Download it, and open the
``.pkg`` file to start the installer.

When done, you'll have a new Python version in ``/Library/Frameworks/Python.framework/Versions/``
that has also been added to your path by the installer.

Uninstalling pyenv
''''''''''''''''''

If you used ``pyenv`` previously, you might want to uninstall the versions you had previously::

    pyenv versions
    pyenv uninstall <version>  # for each installed version

You'll also want to comment out any lines including ``pyenv`` in your ``~/.bash_profile``.

Installing virtualenvwrapper
''''''''''''''''''''''''''''

We use ``virtualenvwrapper`` to help manage Python virtual environments. Install it and set it up
like so::

    /Library/Frameworks/Python.framework/Versions/3.7/bin/pip3.7 install virtualenvwrapper
    cat <<EOF >> ~/.bash_profile
    # to keep stray Python versions from causing problems on Mac OS, we are very explicit about the
    # Python we want to use:
    export PYTHON_BIN=/Library/Frameworks/Python.framework/Versions/3.7/bin/
    export VIRTUALENVWRAPPER_PYTHON=$PYTHON_BIN/python3
    export VIRTUALENVWRAPPER_VIRTUALENV=$PYTHON_BIN/virtualenv
    source $PYTHON_BIN/virtualenvwrapper.sh
    EOF

Note that if you had virtualenv and/or virtualenvwrapper installed for a different Python version
previously, you may need to track it down and remove it (and remove the corresponding ``source``
line from your ``~/.bash_profile``).

Creating a Python Virtual Environment
'''''''''''''''''''''''''''''''''''''

You can now create a virtual environment using a version of Python as follows::

    mkvirtualenv -p python3.7 my-virtualenv-name

for whatever version of Python your project requires. When you need to run anything in this project
simply activate the virtual environment first::

    workon my-virtualenv-name
