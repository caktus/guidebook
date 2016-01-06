.. _minions:

Minions
=======

Within an environment, there's one server, the *master*, that is
running ``salt-master``.

All the servers in the environment also run ``salt-minion`` and are
referred to collectively as *minions*.

What each minion does is defined by editing the list of *roles* in the
minion's salt configuration file ``/etc/salt/minion``.  E.g.::

    grains:
      environment: staging
      roles:
      - salt-master
      - web
      - worker
      - balancer
      - queue
      - cache

The minion with this ``/etc/salt/minion`` file is playing a lot
of roles, and is in the staging environment.

.. warning::

    Removing a role from a minion will NOT automatically undo any
    configuration previously done on the minion.

Some subsets of the minions are defined in ``project._vars.sls`` based
on roles, as follows:

``app_minions``: minions with worker or web roles

``web_minions``: minions with web role

``worker_minions``: minions with worker role

``balancer_minions``: minions with balancer role

.. note::

    What states are applied to servers is controlled directly by their roles.
    These variables are used when the server being configured needs to do something
    for *other* servers with specific roles, such as opening a firewall port so
    that server can connect to this one.
