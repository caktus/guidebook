.. _aws:

Amazon Web Services (AWS)
=========================

We often deploy to Amazon Web Services. Here are some tips on getting started.

AWS Accounts vs. IAM Users
--------------------------

With AWS, we need to be careful to distinguish *AWS accounts* from *IAM users*.

*AWS Accounts* are connected to billing, and to visibility and access to resources.
Caktus has an AWS account. Some of our clients have their own AWS accounts that
we might use when working for those clients, so that they get billed
directly for the resources used instead of us.

*IAM Users* are created within accounts to let administrators
"log into" those accounts and access those resources. IAM Users within
one account are unrelated to IAM users in any other account. If I have
IAM users named "johndoe" in two different AWS accounts, they are completely
separate and different, having nothing to do with each other.

For you to do things in the Caktus AWS account, someone
will have to create an *IAM user* for you within that AWS account, and give it the
privileges for what you need to do.

Root users vs. IAM users
------------------------

Just to confuse things, *AWS accounts* each have a *root user*, which is not
an IAM user within that AWS account, but a user in the global Amazon system of
users - the same set of users that can buy things on Amazon's shopping
sites, in fact. To create a new AWS account, you have to log in as one of
this type of user.

Logging in
----------

To login using a *root user*, there's a global url:
`https://www.amazon.com/ap/signin <https://www.amazon.com/ap/signin>`_.
You can sign in or create a new root user there, and once logged in,
set up billing, create new AWS accounts, buy cat food, etc.

You can tell you're logging in as one of these type of users
because the login page will only prompt for a username and
password.

To login using an *IAM user* in a particular account, you need to go to another page.
These login pages prompt for *three* things: *account*, username,
and password, so you can tell them apart from the "root" user
login page.

Unfortunately, finding a page to login as an *IAM user* can
be tricky. The simplest way is this: each AWS account has
a unique URL that will let you login to that AWS account.
Anyone who is already logged in as an *IAM user* on the account
can find the URL (I think) by going to the
`main *IAM* page <https://console.aws.amazon.com/iam/home>`_
in the AWS console.  Near the top they should see something
like this::

    IAM users sign-in link:
    https://caktus.signin.aws.amazon.com/console

Bookmarking that link will let you sign into that AWS account
using an IAM user. When you follow that link, you *will* be
redirected, and the resulting URL does *not* work directly
to log you into that account, so you cannot just find the signin page once and
bookmark it, you have to track down that original URL.

Anyway, using that link will take you to a three-field login
page with the *Account* field already correctly filled in.
Add the username and password and you will find yourself
logged into the AWS console.

If you know the account identifier, you can change the
account field on this login page to login to another
account, but not all account identifiers are as memorable
as "caktus", some are just long random strings of numbers,
so bookmarking the canonical login URL seems easiest.

AWS Console
-----------

The AWS Console is the web interface to all the AWS services. It
can be overwhelming. Here are some tips for navigating around.

First - you need to know which AWS service you need to work with.
For example, suppose you need to create a new virtual machine.
That AWS service is called "EC2". In the AWS console, click the
orange cube that appears in the top left of every page, and you'll
end up at a directory of AWS services. It's also overwhelming :-),
but if you don't spot EC2 right away, you can search in the browser
page for it. When you find it, click it, and you'll be in the part
of the AWS console where you can manage EC2.

*Unfortunately*, not everything we think of as an AWS service
is listed on that directory page (believe it or not). For example, quite a few
services are managed within the EC2 part of the AWS console - such
as Security Groups, Elastic Load Balancers, Elastic IPs, Autoscaling
Groups, etc.  You can see them listed down the left side of the
EC2 interface.

So, if you don't see the service you want on the main directory
of services, try within the EC2 part of the console.

Regions
-------

Another important concept to understand from the beginning
is the *AWS Region*. You can think of an AWS Region as a
geographic location where Amazon has a bunch of data
centers. There are regions with names like "US East (N. Virginia)",
"EU (Ireland)", "EU (Frankfurt)", etc.

With most AWS services, you can create and use resources in
any region you like, but to manage them, you first have to
select one region using the dropdown near the top right of
every page. Once you've selected a region, you will only see
resources from that region, and new resources you create will
be created in that region, until you select a different region.

Tip: You can have multiple browser tabs/windows open
to the AWS console with different regions selected, if that
helps on really big projects to keep an eye on everything.
But usually you won't have to do that.

We typically try to create resources in a region closest
to the majority of the site's users. If we can't pick a
region that way, we usually end up in "US East (N. Virginia)"
just because it seems to be the default.

.. WARNING::
    Not every service is available in every region.
    Before you start setting up a great big infrastructure in some
    region, it's a good idea to verify that all the services
    you will need are available there. You don't want the
    services that make up your site to have to communicate
    between regions if you can help it.

