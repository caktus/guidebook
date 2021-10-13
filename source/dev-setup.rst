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

    % xcode-select --install

Get more information about the Command Line Tools directly from Apple:

    https://developer.apple.com/library/ios/technotes/tn2339/_index.html#//apple_ref/doc/uid/DTS40014588-CH1-WHAT_IS_THE_COMMAND_LINE_TOOLS_PACKAGE_


Homebrew
''''''''

Homebrew is a project that provides automated download, compilation, and install of a wide range
of developer and console tools for the Mac.

A self-executing install script can be fetched and run simply, from the Homebrew documentation::

    % /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

You can receive more information in the Homebrew documentation or see a full list of packages
available once you've installed it.

* Homebrew Docs: https://github.com/Homebrew/homebrew/tree/master/share/doc/homebrew#readme
* Package List: https://github.com/Homebrew/homebrew/tree/master/Library/Formula

OpenSSL
'''''''

There are known incompatibilies with the OpenSSL library shipped with OSX, but Homebrew gives us
a more up-to-date version to link against. We need to both install and force-link this one::

    % brew install openssl

Version Control
'''''''''''''''

Install Git, the version control system used by 
projects to obtain and coordinate changes to the code base between all
developers::

    % brew install git

**Note:** git may have already been installed with ``xcode-select``. 
To test run::

    % git --version
    % git version 2.29.0

PostgreSQL
''''''''''

The first important package to install from Homebrew is the PostgreSQL database and the PostGIS
extensions::

    % brew install postgresql
    % brew install postgis

With PostgreSQL installed, you'll want to make sure it runs every time your machine comes up, and
to start it running immediately::

    % mkdir -p ~/Library/LaunchAgents
    % cp /usr/local/Cellar/postgresql/$(postgres --version|cut -d' ' -f3)/homebrew.mxcl.postgresql.plist ~/Library/LaunchAgents/
    % launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist

Alternatively homebrew can manage starting the postgresql service. 
Add the following to your ``~/.zshrc`` file if you are using the default zsh shell::

    # start the postgresql service
    brew services start postgresql

**Note:** 
For changes to take effect in your current shell instance after updating the ``~/.zshrc`` file you must run::

    % source ~/.zshrc

If you have chosen to use homebrew to run the postgresql service you can test that it is running with this command::

    % brew services list
    Name          Status  User        Plist
    postgresql@10 started <user> /Users/<user>/Library/LaunchAgents/homebrew.mxcl.postgresql.plist

Python
''''''

Mac OS X installers for all the latest Python versions can be downloaded from:
https://www.python.org/downloads/mac-osx/

Practically speaking (as of September 2021, at least), it is helpful to have Python 3.7, 3.8,
and 3.9 all installed locally (soon, probably 3.10 as well).

On the Mac OS X installer download page, find the "macOS 64-bit installer" link for the latest
point release of the Python major version that you want to install. Download it, and open the
``.pkg`` file to start the installer.

When done, you'll have a new Python version in ``/Library/Frameworks/Python.framework/Versions/``
that has also been added to your path by the installer.

Uninstalling pyenv
''''''''''''''''''

If you used ``pyenv`` previously, you might want to uninstall the versions you had previously::

    % pyenv versions
    % pyenv uninstall <version>  # for each installed version

You'll also want to comment out any lines including ``pyenv`` in your ``~/.zshrc``.

Installing virtualenvwrapper
''''''''''''''''''''''''''''

We use ``virtualenvwrapper`` to help manage Python virtual environments. Install it and set it up
like so::

    # determine the location of the python version you want associated with virtualenvwrapper
    % which python3.9
    /Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9
    # use this python version to install virtualenvwrapper
    % python3.9 -m pip install virtualenvwrapper
    # ensure virtualenv was installed to the same /bin directory as your python version
    % which virtualenv
    /Library/Frameworks/Python.framework/Versions/3.9/bin/virtualenv
    # create a private directory where your virtualenvs will be stored
    % mkdir ~/.virtualenvs
    # Now we will add the following configuration to our .zshrc file
    % cat <<EOF >> ~/.zshrc
    % export WORKON_HOME=~/.virtualenvs
    % export PYTHON_BIN=/Library/Frameworks/Python.framework/Versions/3.9/bin/
    % export VIRTUALENVWRAPPER_PYTHON=$PYTHON_BIN/python3
    % export VIRTUALENVWRAPPER_VIRTUALENV=$PYTHON_BIN/virtualenv
    % source $PYTHON_BIN/virtualenvwrapper.sh
    % EOF
    % source ~/.zshrc

Note that if you had virtualenv and/or virtualenvwrapper installed for a different Python version
previously, you may need to track it down and remove it (and remove the corresponding ``source``
line from your ``~/.zshrc``).

To switch python versions that 

Creating a Python Virtual Environment
'''''''''''''''''''''''''''''''''''''

You can now create a virtual environment using a version of Python as follows::

    % mkvirtualenv -p python3.9 my-virtualenv-name

for whatever version of Python your project requires. When you need to run anything in this project
simply activate the virtual environment first::

    % workon my-virtualenv-name

to deactivate run::
    % deactivate

NVM
'''

Node Version Manager allows us to switch seamlessly between different node.js versions.
To install run::

    % brew install nvm
    % mkdir ~/.nvm

Update the ``.zshrc`` file::

    # NVM
    export NVM_DIR="$HOME/.nvm"
    [ -s "/usr/local/opt/nvm/nvm.sh" ] && . "/usr/local/opt/nvm/nvm.sh"  # This loads nvm
    [ -s "/usr/local/opt/nvm/etc/bash_completion.d/nvm" ] && . "/usr/local/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion
