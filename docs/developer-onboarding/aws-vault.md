Multi-factor Authentication on the Command Line using AWS-Vault
===============================================================

Slow Your Scroll - The Introduction
-----------------------------------

Having some form of Multi-factor Authentication (MFA) enabled, be it
sms, an authenticator app, or yubikey, is an important aspect of the
account security policy that you enforce on your AWS Account. User
Credentials (username and password) and MFA give users a higher degree
of certainty that the AWS Console user accessing resources within the
account is in fact who they say they are. As developers and system
administrators it\'s important that we extend this degree of certainty
to the command line (cli) where we interact with aws resources
programmatically using access keys. This can be done using
[aws-vault](https://github.com/99designs/aws-vault) a cli tool to
securely store and access AWS credentials in a development environment.

To Install
----------

MacOS

:   `brew install --cask aws-vault`

Windows

:   `choco install aws-vault`

Linux

:   please refer to [install
    section](https://github.com/99designs/aws-vault#installing) of
    aws-vault docs for your linux distribution

Getting Started - A Quick Look at the AWS Config File
-----------------------------------------------------

Open `~/.aws/config`.

```config
; Caktus Managed AWS
[profile caktus]
credential_process=aws-vault exec --no-session --json caktus

[profile caktus-mfa]
mfa_serial=arn:aws:iam::112250541543:mfa/<username>
source_profile=caktus
region=us-east-1
output=json

; Assume Role setup

[profile <role-profile>]
role_arn=arn:aws:iam::<role-profile-account-id\>:role/<assumed-role>
source_profile=<default-profile-mfa\> region=us-east-1

[profile <role-profile>]
role_arn=arn:aws:iam::<role-profile-account-id>:role/<assumed-role>
source_profile=<default-profile-mfa>
```


At the end of this setup you should have both a default profile and mfa
profile for main account access listed in your aws config file. Assuming
roles in other accounts should follow the above syntax that sets
`<default-profile-mfa>` as the `source_profile` for the
`<role_profile>`. Both `Main Account setup` and `Assume Role setup` can
be repeated as many times as needed. You will need to comment out (`;`)
or delete an existing `<default-profile>` to allow `aws-vault` to manage
this profile.

Main Account setup
------------------

1.  Setup `<default-profile>` by running
    `aws-vault add <default-profile>`.

::

:   \# Here our default-profile is called \"test\" \$ aws-vault add test
    Enter Access Key ID: \<aws-access-key-id\> Enter Secret Access Key:
    \<aws-secret-access-key\> Added credentials to profile \"test\" in
    vault

After providing your aws keys you will be prompted by KeyChain on MacOS
to provide your user\'s password. If you are on another operating system
or would like to change the behavior of the vaulting backend please
refer to
[this](https://github.com/99designs/aws-vault#vaulting-backends) section
of the docs.

In the `~/.aws/config`, you should see the newly created
`<default_profile>`.

::

:   \[profile test\]

2.  Set the `credentials_process` variable to instruct `aws-vault` to
    expose the `default-profile`\'s access keys to the terminal.

::

:   \[profile test\] credential_process=aws-vault exec \--no-session
    \--json test

3.  Setup `<default-profile-mfa>` in `~/.aws/config`

::

:   \[profile test\] credential_process=aws-vault exec \--no-session
    \--json test

    ; Example test account id: 111111111 \[profile test-mfa\]
    mfa_serial=arn:aws:iam::111111111:mfa/test-user source_profile=test
    region=us-east-1 output=json

Setting `mfa_serial` for the mfa profile: \* Copy your IAM ARN for your
user: `arn:aws:iam::<account-id>:user/test-user` \* Replace `user` with
`mfa`: `arn:aws:iam::<account-id>:mfa/test-user`

The `<default_profile-mfa>`\'s `source profile` should be set to the
`<default_profile>`. In the above example, profile `test-mfa` has its
`source_profile` set to `test`.

`<default_profile-mfa>` can just be added to the aws config file.
`aws-vault add <profile>` is not used.

4.  Test the configuration

::

:   \$ aws-vault exec test-mfa Enter MFA code for
    arn:aws:iam::111111111:mfa/test-user: \<Enter Code from MFA Device\>
    \# Now authenticated and aws-vault session has been created \$ aws
    s3 ls \<lists S3 buckets in AWS Account\>

Recommended Background Reading
------------------------------

If you would like to have a fuller understanding of what\'s going on
under the hood, I recommended these resources.

**Resources:** - Kyle Knapp\'s [2017 AWS Reinvent
talk](https://youtu.be/W8IyScUGuGI?t=1251) - [AWS Knowledge Center: How
do I use an MFA token to authenticate access to my AWS resources through
the AWS
CLI?](https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/)
- [Sourcing credentials with an external
process](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html)
