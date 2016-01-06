Adding Margarita to a project that uses Salt
============================================

Invoking the states
-------------------

You'll apply the states to your servers by configuring your ``top.sls``
file in your main directory of salt states (often ``/srv/salt/top.sls``).

Here's an example from an actual project. You can see that we apply
some SLS files to all servers (the ones under ``'*'``), some to only
one environment (``'environment:local'``), and some to only certain
roles. It's okay to mention an SLS file more than once; it'll only be
applied once to a given system.

    base:
      '*':
        - base
        - sudo
        - sshd
        - sshd.github
        - locale.utf8
        - project.devs
        - newrelic_sysmon
        - forward_logs
      'environment:local':
        - match: grain
        - vagrant.user
      'roles:salt-master':
        - match: grain
        - salt.master
      'roles:web':
        - match: grain
        - project.postgres
        - project.web.app
        - project.web.npm
        - elasticsearch
        - project.manage_index
        - newrelic_npi
        - django_reversion
        - statsd
      'roles:worker':
        - match: grain
        - project.postgres
        - project.worker.default
        - project.worker.beat
        - elasticsearch
        - newrelic_npi
        - django_reversion
        - statsd
      'roles:balancer':
        - match: grain
        - project.web.balancer
      'roles:queue':
        - match: grain
        - project.queue
      'roles:cache':
        - match: grain
        - project.cache



Making Margarita available to Salt
----------------------------------

To be able to use the states from Margarita, we need to
add the tree of files from Margarita somewhere
that Salt looks for SLS files.

We've tried using Salt's gitfs support for this, but found it
to be too unreliable in noticing updates, not to mention
inconvenient for test and development.

A better approach seems to be to check it out into a local
directory on the Salt master, and add that directory to
the file roots.  So part of your ``/etc/salt/master`` file
might look like::

    fileserver_backend:
      - roots

    file_roots:
      base:
        - /srv/salt
        - /srv/margarita

Then you might have a Salt state to put Margarita into that
directory at a given version, maybe something like this::

    git-install:
      pkg.installed:
        - name: git-core

    clone_repo:
      cmd.run:
         - name: git clone https://github.com/caktus/margarita.git margarita
         - user: root
         - unless: test -e /srv/margarita/.git
         - cwd: /srv
         - requires:
           - pkg: git-install

    fetch_repo:
      cmd.run:
         - name: git fetch origin
         - user: root
         - cwd: /srv/margarita
         - requires:
            - cmd: clone_repo
            - pkg: git-install

    reset_repo:
      cmd.run:
         - name: git reset --hard {{ pillar['margarita_version'] }}
         - user: root
         - cwd: /srv/margarita
         - requires:
            - cmd: fetch_repo

Just be sure to restart the salt-master after Margarita is updated.
We do that outside Salt after invoking this state, something
like this::

    sudo salt -G 'roles:salt-master' state.sls margarita
    sudo service salt-master restart

(Note: the Margarita salt state above could be simplified using
Salt's built-in support for ``git``, but this approach seems to
be most reliable, and we can see exactly what it does and how it
works.)
