# AWS Setup

AWS is a core component of our deployment and management stack. We use it for just about everything.

## Steps

### Obtain an AWS account from Tech Support

You can go about this in various ways. Politely request to be given an AWS use account.

1. Email: `support@caktusgroup.com`
1. Slack: `#sysadmin` channel.

### Obtain your credentials from your account.

1. Sign into [https://caktus.signin.aws.amazon.com/console](https://caktus.signin.aws.amazon.com/console)
1. Using the credentials provided, setup Mulit-Factor Authentication.
1. Navigate to your [Security Credentials](https://console.aws.amazon.com/iam/home#/security_credentials)
1. Click `Create Access Key`


!!! warning

    Be sure that you download the csv offered to you in the confirmation modal, otherwise you will need to re-do it as you won't have another opportunity to read the secret key.

### Setup AWS command line

!!! note

    Some projects have the AWS cli installed as a pip dependency. If so, you will have `1.n.n` version of AWS cli. If you install using the below instructions, you will have `2.n.n` version. This is not a problem both are supported. V2 has some extra sugar that's all.

#### Install the CLI 

    Follow the [Install the CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) instructions for your machine. Are you on an M1? Have you followed the [blog post](M1.md) yet?

#### Verify your installation

```shell
    (prompt)$ which aws
```
    
That should read something like `/usr/local/bin/aws`
    
```shell
    (prompt)$ aws --version
```
    
That should be something like `aws-cli/2.n.n ...`

### Configure AWS command line

!!! note 
    
    Caktus uses an AWS assume role to grant access to the resouces necessary to manage our projects. Project specific documentation and `arn`s can be found [here](https://github.com/caktus/caktus-hosting-services/blob/main/docs/aws-assumerole.md#aws-accounts)

#### Create the directories and files for AWS

```shell
    (prompt)$ mkdir ~/.aws
    (prompt)$ touch ~/.aws/credentials
    (prompt)$ touch ~/.aws/config
```

#### Set profile and credentials 

You will need a primary profile named `caktus` in your `config` and `credentials` file

```shell
    # ~/.aws/config
    [profile caktus]
    region = us-east-1
```

```shell
    # ~/.aws/credentials
    [caktus]
    aws_access_key_id = <SECRET KEY FROM THE CSV YOU DOWNLOADED>
    aws_secret_access_key = <SECRET ACCESS KEY FROM THE CSV YOU DOWNLOADED>
```

#### Project Profiles

Each project will have an [Role ARN](https://github.com/caktus/caktus-hosting-services/blob/main/docs/aws-assumerole.md#aws-accounts) that you will use
to access your projects.  For each project you work on you will need a `config` and `credentials` entry.

```shell
    # ~/.aws/config

    [profile my-caktus-project]
    region = <project-region> 
```

```shell
    # ~/.aws/credentials
    [caktus]
    aws_access_key_id = <SECRET KEY FROM THE CSV YOU DOWNLOADED>
    aws_secret_access_key = <SECRET ACCESS KEY FROM THE CSV YOU DOWNLOADED>
    
    ...

    [my-caktus-project]
    role_arn = <ARN FROM THE ABOVE "Role Arn" LINK>
    source_profile = caktus
```

#### Test your access

To make sure you have everything set up correctly, test your access:

```shell
    (prompt)$ export AWS_PROFILE=my-caktus-project
    (prompt)$ aws s3 ls
```

Depending on whether or not the project has S3 buckets you should see a list of them. Regardless you should not see an error.

