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

    brew install postgres
    brew install postgis

With PostgreSQL installed, you'll want to make sure it runs every time your machine comes up, and
to start it running immediately::

    mkdir -p ~/Library/LaunchAgents
    cp /usr/local/Cellar/postgresql/$(postgres --version|cut -d' ' -f3)/homebrew.mxcl.postgresql.plist ~/Library/LaunchAgents/
    launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist

Python
''''''

Pyenv via brew

    brew install pyenv

Different projects require different versions of Python. Some older projects will still be using
Python 3.7, and newer projects are eiter on 3.5 or 3.6, so we'll install the latest versions of all
three.

    pyenv install $(pyenv install -l | grep " 2.7" | tail -n 1)
    pyenv install $(pyenv install -l | grep " 3.5" | tail -n 1)
    pyenv install $(pyenv install -l | grep " 3.6" | tail -n 1)

And link them so they'll be in your path.

    ln -s ~/.pyenv/versions/$(pyenv install -l | grep " 2.7" | tail -n 1 | strip-indent)/bin/python /usr/local/bin/python2.7
    ln -s ~/.pyenv/versions/$(pyenv install -l | grep " 3.5" | tail -n 1 | strip-indent)/bin/python /usr/local/bin/python3.5
    ln -s ~/.pyenv/versions/$(pyenv install -l | grep " 3.6" | tail -n 1 | strip-indent)/bin/python /usr/local/bin/python3.6


Python Packages and Environments
''''''''''''''''''''''''''''''''

Finally, every project will use the tools `pip`, `virtualenv`, and
`virtualenvwrapper` to manage sandboxes for each project and the Python
packages required for each project installed into those sandboxes.

You'll install `pip` first, into your system Python that comes with OSX::

    sudo easy_install pip

And, using pip, install `virtualenvwrapper` which will automatically
install `virtualenv` as one of its dependencies::

    sudo pip install virtualenvwrapper --ignore-installed six

Virtualenv Wrapper requires some configuration to work with your local
command line shell. You can copy and paste the code below to set this up
in your Terminal. (You can also customize what you set PROJECT_HOME to, if
you wish)::

    echo "export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile
    source ~/.bash_profile

Creating a Python Virtual Environment
'''''''''''''''''''''''''''''''''''''

You can create a virtual environment using a version of Python as follows::

    mkvirtualenv -p $(which python) my-virtualenv-name

Or

    mkvirtualenv -p $(which python3) my-virtualenv-name
