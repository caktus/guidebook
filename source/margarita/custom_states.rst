Custom Salt States
==================

These are new states you can use in your SLS files after installing Margarita.

.. _ufw:

ufw
~~~

Usage::

    ufw_policy:
      ufw.default:
        - policy: deny

    ufw_status:
      ufw.enabled:
        - enabled: true

    ufw.allow:
      - enabled: true
      - proto: tcp
      - names:
         - '22'
         - '80'
         - '443'

or::

    ssh:
      ufw.allow:
        - name: '22'
        - enabled: true

.. _watchlog:

watchlog
~~~~~~~~

Custom state for monitoring plaintext log files
and forwarding to syslog.

See: http://www.rsyslog.com/doc/v8-stable/configuration/modules/imfile.html

Usage::

    watch_my_log:
      watchlog.file:
        - name: watch_my_log
        - path: /path/to/file.log
        - enable: true|false
        - tag: my_log
        - facility: local0
        - severity: info
        - requires:
          - syslog

This works by creating a new conf.d file for
`rsyslog <http://www.rsyslog.com>`_
(if enable is true) or removing one if it exists (if enable
is false). The name of the file is always ``<name>.conf`` and it
goes in the ``/etc/rsyslog.d/`` directory. If anything is changed,
rsyslog is told to reload.


At least rsyslog v8 must be installed. The state checks for
this and will return an error otherwise.  Also, the ``imfile``
rsyslog module must be loaded. The state checks for this too,
and will include the expected syntax in the error message if
the check fails.

There's a Margarita state :ref:`syslog` that will ensure both of
those requirements are met; just make your state depend on
that.

Required parameters
-------------------

Name: name of the state like for any Salt state. Used to derive
the name of the rsyslog config file to create.

Path: Path to the log file to monitor. The filename part can
include wildcards (e.g. ``/var/log/myapp/*.log``), but not any
intermediate parts (you can't use ``/var/log/*/error.log``).

Enable: ``true`` to ensure monitoring is set up. ``false``
to ensure monitoring is not set up.

If you don't want a log monitored anymore, don't just delete
the state; change ``enable`` to false, apply the state to the
systems where the log was being monitored so that the config
file gets removed, and only then delete the state from your
config.

Facilities: 'local0', 'local1', 'local2', 'local3', 'local4',
'local5', 'local6', 'local7'.  (Or any other syslog facility,
but the others are supposed to be reserved for specific
uses.)

Severities: 'emerg', 'alert', 'crit', 'err', 'warning',
'notice', 'info', 'debug'.

Tag: Any string (probably not a good idea to include spaces though).

Optional parameters
-------------------

There are no optional parameters that are specific to this
state, but you can add the usual universal ones like
``requires``.
