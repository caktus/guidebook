# Account Configuration

## Configure AWS

### Setting up a Client sub account

If a client needs to have a sub account created for us to use with our assume roles. Follow these instructions.

[First create the sub-account from the organizations root account](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_create.html)

Once that is done they will need to log in and do some more work. It is not obvious how to sign in to the sub-account
after they are done with creating it. [Follow these instructions](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html)


### TODO: instructions on how to configure the sub-account for the AssumeRole


## Configure Local project

### Add Configured Account to AWS Configs
Once the sub-account and AssumeRole have been configured set up your local AWS_PROFILE

Currently, we keep information about the account in two places `~/.aws/config` and `~/.aws/credentials`.

`config` is where the profile name, and the account region are defined.
`credentials` is where we assign the AssumeRole information and link that with caktus IAM credentials.

#### Config

Edit the config file, and add a section for the aws account, usually this is some form of the project name.

```yaml
[profile <project_name>]
region = <project_region>
```

#### Credentials
```yaml
[<profile_name_from_config>]
role_arn = arn:aws:iam::<DIGITS>:role/CaktusAccountAccessRole-Admins
source_profile = caktus
```

