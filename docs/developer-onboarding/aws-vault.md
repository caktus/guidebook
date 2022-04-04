# Multi-factor Authentication on the Command Line using AWS-Vault

## Slow Your Scroll - The Introduction

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

## To Install

MacOS

`brew install --cask aws-vault`

Windows

`choco install aws-vault`

Linux

please refer to [install section](https://github.com/99designs/aws-vault#installing) of 
aws-vault docs for your linux distribution

## Getting Started - A Quick Look at the AWS Config File

Open `~/.aws/config`.

```ini
; Caktus Managed AWS
[profile caktus]
credential_process=aws-vault exec --no-session --json caktus

[profile caktus-mfa]
mfa_serial=arn:aws:iam::<caktus-account-id>:mfa/<username>
source_profile=caktus
region=us-east-1
output=json

; Assume Role setup

[profile <role-profile>]
role_arn=arn:aws:iam::<role-profile-account-id>:role/<assumed-role>
source_profile=caktus-mfa
region=us-east-1

[profile <role-profile>]
role_arn=arn:aws:iam::<role-profile-account-id>:role/<assumed-role>
source_profile=caktus-mfa
```


At the end of this setup you should have both a caktus profile and mfa
profile for main account access listed in your aws config file. Assuming
roles in other accounts should follow the above syntax that sets
`caktus-mfa` as the `source_profile` for the
`<role_profile>`. Both `Main Account setup` and `Assume Role setup` can
be repeated as many times as needed. 

You will need to comment out (`;`)
or delete an existing `caktus` profile to allow `aws-vault` to manage
this profile in the config file. No changes are needed to be done
to the credentials file.

## Caktus Account setup

1.  Setup `caktus` by running
    `aws-vault add caktus`.

```
$ aws-vault add caktus
Enter Access Key ID: <aws-access-key-id> 
Enter Secret Access Key: <aws-secret-access-key> 
Added credentials to profile "caktus" in vault
```

After providing your aws keys you will be prompted by KeyChain on MacOS
to set a password or provide your apple id password. If you are on another operating system
or would like to change the behavior of the vaulting backend please
refer to [this](https://github.com/99designs/aws-vault#vaulting-backends) section
of the docs.

In the `~/.aws/config` file, you should see the newly created
`caktus` profile.

```
[profile caktus]
```

2.  Set the `credentials_process` variable to instruct `aws-vault` to
    expose the `caktus` profile's access keys to the terminal.
```
[profile caktus]
credential_process=aws-vault exec --no-session --json caktus
```

3.  Setup `caktus-mfa` in `~/.aws/config` file

```
[profile caktus]
credential_process=aws-vault exec --no-session --json caktus

[profile caktus-mfa]
mfa_serial=arn:aws:iam::<account-id>:mfa/<username>
source_profile=caktus
region=us-east-1
output=json
```

Setting `mfa_serial` for the caktus-mfa profile:
- Copy your IAM ARN for your
user: `arn:aws:iam::<caktus-account-id>:user/<username>`
- Replace `user` with `mfa`: `arn:aws:iam::<caktus-account-id>:mfa/<username>`

The `caktus-mfa` profile's `source profile` should be set to `caktus`.

`caktus-mfa` can just be added to the aws config file.
`aws-vault add caktus-mfa` is not used.

4.  Test the configuration

```
$ aws-vault exec caktus-mfa 
Enter MFA code for arn:aws:iam::<caktus-account-id>:mfa/<username>: <Enter Code from MFA Device>
# Now authenticated and aws-vault session has been created 
$ env | grep AWS
AWS_VAULT=caktus-mfa
...
...
...
```

5. Assuming Roles from the Caktus Account

```
[profile <role-profile>]
role_arn=arn:aws:iam::<role-profile-account-id>:role/<assumed-role>
source_profile=caktus-mfa
region=us-east-1
```

Asumming roles will follow the above pattern. Check with the lead developer for the particular project you are joining
to get the `<role-profile-account-id>` and `<assumed-role>` that you will be assuming. For example, here is
how you would update `~/.aws/config` to assume the role assoicated with the `saguaro-cluster`.

```
[profile saguaro-cluster]
role_arn=arn:aws:iam::<saugaro-cluster-account-id>:role/CaktusAccountAccessRole-Admins
source_profile=caktus-mfa
region=us-east-1
```

6. Assume the Role

```
# Assumption: You have already authenticated by running "aws-vault exec caktus-mfa".
# Let's check
$ env | grep AWS
AWS_VAULT=caktus-mfa
...
...
# Let's unset the AWS_VAULT environment variable
$ unset AWS_VAULT
# let's switch to the saguaro-cluster role
$ aws-vault exec saguaro-cluster
# Ensure that you have access to the AWS Account
$ aws s3 ls
<list of s3 buckets within this account>
```

* If you are switching profiles, make sure to run `unset AWS_VAULT` before running `aws-vault exec <role_profile>`.
* If `AWS_VAULT` is not set then you can assume what ever mfa-enabled profile you would like.

7. Caktus CI/CD Pipeline

AWS Vault does not replace the need to set `AWS_PROFILE` as well when running manual deployments or ansible scripts locally.
Make sure to `export AWS_PROFILE` when deploying resources.




## Recommended Background Reading

If you would like to have a fuller understanding of what\'s going on
under the hood, I recommended these resources.

**Resources:** 
* Kyle Knapp\'s [2017 AWS Reinvent
talk](https://youtu.be/W8IyScUGuGI?t=1251)
* [AWS Knowledge Center: How do I use an MFA token to authenticate access to my AWS resources through
the AWS CLI?](https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/)
* [Sourcing credentials with an external process](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html)
