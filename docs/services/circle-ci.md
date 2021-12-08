Circle CI
=========

The project template now has a Circle CI template that you can use for
your project. Circle CI\'s benefit over Travis CI is that it works for
private non-Caktus repos. Once you have completed the initial project
setup (i.e. the items in README.rst), do the following:

1.  If you don\'t have one already, [create a Circle CI
    account.](https://circleci.com/) Circle CI uses Github accounts for
    authentication, so when you sign up, be sure to sign up with your
    Caktus github account.
2.  Find your project on the [projects
    page](https://circleci.com/add-projects). Any repos that you have
    admin access to, across organizations, should be visible there. You
    may need to refresh your list by clicking the \'Reload
    repositories\' button, especially if the repo was created very
    recently. Enable your repo on this page. This will kick off a build
    of the default branch of the repo, which will most likely fail,
    since that branch doesn\'t yet have a `circle.yml` file. Don\'t
    worry\... we\'ll fix it.
3.  Review the `circle.yml` file at the top level of the repo. Update it
    to match the specifics of your project.
4.  Set up HipChat notifications.
    A.  Get the Hipchat Room Number. This is the number in the URL bar
        when you are looking at the room in Hipchat.
    B.  Obtain the HipChat API token for Circle CI. Click on the
        \'\...\' button in the upper right-hand corner of your HipChat
        room page, then click on \'Integrations\...\', then click on the
        \'Installed\' button to filter by already-installed
        integrations. You should see Circle CI listed there. Click on it
        and you will find the Token. If you don\'t have access, create a
        [support
        request](https://caktus.atlassian.net/servicedesk/customer/portal/3)
        to get one.
    C.  Navigate in Circle CI to your project and then click on the
        \'settings\' icon in the upper right which should take you to
        project settings. Click on \'Chat Notifications\' and fill in
        the Room Number and API Token from the above 2 steps. Click
        \'Save\'.
5.  Commit the changes to your `circle.yml` file and push that commit to
    github. That should trigger a build and you should see the result of
    that build in your HipChat room, once complete.
