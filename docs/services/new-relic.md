New Relic
=========

To enable New Relic monitoring for an environment:

1.  Get a license key. This can be found in the New Relic web interface.
    We have multiple subaccounts, some of which are free and some of
    which cost money to use, so make sure you first select the correct
    subaccount. Log in to New Relic and click on the dropdown menu in
    the upper right corner. Use the 'Switch account' submenu to choose
    your subaccount. Once you have switched to your subaccount, go back
    to the dropdown menu and click on 'Account settings'. The license
    key will be listed on that page. If you don't have access to New
    Relic or are unsure of which New Relic subaccount to use, create a
    [support
    request](https://caktus.atlassian.net/servicedesk/customer/portal/3)
2.  Generate an encrypted variable `NEW_RELIC_LICENSE_KEY` containing
    the license key for each environment:

    ``` {.sourceCode .bash}
    ~/dev/myproject$ fab staging encrypt:NEW_RELIC_LICENSE_KEY='abc123'
    "NEW_RELIC_LICENSE_KEY": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hIwDi3G8b0sD8fkBA/4kMuhn2YmdKhyy99Xi3Nn6XOUmY/oikyU1AF68ynHfywNd
      zcu8xcA0iHhj/eK7dDvC9eE94xUNNoPkddU+J6ulzhEIzQFWndD5YCO1WyHWLYbq
      N48BPaiUHWoiWFKA4aApPJHPfiV6JJUxiwHadhoAseOQw94ce75fUqbe4RiXrNJS
      ATFNQz0dtCF8H0VhYBUYHvF7yHuhZVeOqgTT93B0tDGCy9rq47Dq3PnjityrFuAL
      TLNW7zsjjEuA1P6HZ8xwRqYwSJ4MF8tkXDUX3Q++cGlW6w==
      =w3nx
      -----END PGP MESSAGE-----
    ```

3.  Put that in the proper environment's SLS file, in the `secrets`
    dictionary:

    ``` {.sourceCode .yaml}
    # <environment>.sls
    secrets:
      "NEW_RELIC_LICENSE_KEY": |-
        -----BEGIN PGP MESSAGE-----
        -----END PGP MESSAGE-----
    ```

4.  Add any other custom [New Relic configuration
    variables](https://docs.newrelic.com/docs/agents/python-agent/installation-configuration/python-agent-configuration#environment-variables)
    under `env:`. The default values for most will probably work well
    for most projects, but you should definitely include a setting for
    NEW_RELIC_APP_NAME, as failure to provide a value for this may
    result in your project unexpectedly showing up under some other
    pre-existing application being monitored by the license key's
    account. Here are some examples of how to set new relic
    configuration variables:

    ``` {.sourceCode .yaml}
    # project.sls
    env:
      NEW_RELIC_MONITOR_MODE: "false"

    # <environment>.sls
    env:
      NEW_RELIC_APP_NAME: myproject <environment>
      NEW_RELIC_MONITOR_MODE: "true"
    ```

    Be sure to quote "true" and "false" as above, to avoid Salt/YAML
    turning these into real Booleans; we want the strings "true" or
    "false" in the environment.

    You can put some values in `project.sls` and others in
    `<environment>.sls`. Just be consistent for a given key; if the same
    key is present in both `project.sls` and the current
    `<environment>.sls` file, Salt makes no guarantees about which value
    you'll end up with.

    Note that any environment where `NEW_RELIC_LICENSE_KEY` is not set
    will not include any New Relic configuration, so it's safe to put
    other settings in `project.sls` even if you're not using New Relic
    in every environment.

5.  If you are using elasticsearch and would like New Relic monitoring
    of that as well, add to the pillar somewhere.

    ``` {.sourceCode .yaml}
    # project.sls or <environment>.sls
    elasticsearch_newrelic: true
    ```

    The plugin will get set up automatically if that pillar setting is
    present, and you are using the `elasticsearch` margarita state in
    your `top.sls` file.

6.  Add state `newrelic_sysmon` to your Salt `top.sls` in the `base`
    section (for all servers). It's safe to add that unconditionally
    for all environments; it's a no-op if no New Relic license key has
    been defined:

    ``` {.sourceCode .yaml}
    base:
      '*':
        - ...
        - newrelic_sysmon
    ```

7.  Be sure `newrelic` is in the Python requirements of the project
    (likely in `requirements/production.txt`):
    <https://pypi.python.org/pypi/newrelic>
