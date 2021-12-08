Travis CI
=========

The project template now has a Travis CI template that you can copy for
your project. Once you have completed the initial project setup (i.e.
the items in README.rst), do the following:

1.  Rename the template to `.travis.yml`. (Note: The existing file named
    `.travis.yml` in the project template is for testing the template
    itself, so it is fine to overwrite it):

    ``` {.sourceCode .bash}
    ~/dev/myproject$ mv project.travis.yml .travis.yml
    ```

2.  If you don\'t have one already, [create a Travis CI
    account](https://travis-ci.org), being sure to link it to your
    Caktus github account.
3.  Find your project on your [profile
    page](https://travis-ci.org/profile/). Any repos that you have admin
    access to, across organizations, should be visible there. You may
    need to refresh your list by clicking the \'Sync account\' button,
    especially if the repo was created very recently. Enable your repo
    on this page.
4.  Review the `.travis.yml` template that you copied. Update it to
    match the specifics of your project (e.g. Python version, PostgreSQL
    version). Some settings are commented out and can be uncommented if
    they apply to your project. The one section that WILL need to be
    updated is the notifications section. See below.
5.  Set up HipChat notifications.
    A.  Obtain a HipChat API token and Room ID. You may be able to get
        this by clicking on the \'\...\' button in the upper right-hand
        corner of your HipChat room page, and then clicking on
        \'Integrations\...\' and then clicking on the \'Travis CI\'
        button. If you don\'t have access, create a [support
        request](https://caktus.atlassian.net/servicedesk/customer/portal/3)
        to get one.
    B.  Install the `travis` command line tool:
        <https://github.com/travis-ci/travis.rb#installation>
    C.  Use the HipChat API token and Room ID obtained in step A to
        generate an encrypted token:

        ``` {.sourceCode .bash}
        ~/dev/myproject$ travis encrypt <api_token@room_id>
        Please add the following to your .travis.yml file:

          secure: "... long encrypted value ..."
        ```

    D.  Copy that value into the place indicated in the template
        `.travis.yml` file.
    E.  Since the value is encrypted, it is safe for this to be in a
        public github repo.

6.  Commit the changes to your `.travis.yml` file and push that commit
    to github. That should trigger a build and you should see the result
    of that build in your HipChat room, once complete.
