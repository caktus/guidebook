# Amazon Web Services (AWS)


## Encryption by default

Configure your AWS account to enforce the encryption of new EBS volumes and snapshots. A few notes:

* You can launch an instance only if the instance type supports EBS encryption when you enable encryption by default.
* Encryption by default is a region-specific setting.

Follow the [Encryption by default instructions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#encryption-by-default) or you can use the AWS CLI. For example:

```shell
aws --region us-west-1 ec2 enable-ebs-encryption-by-default
```


## Setting up a Client sub account

If a client needs to have a sub account created for us to use with our assume roles. Follow these instructions.

[First create the sub-account from the organizations root account](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_create.html)

Once that is done they will need to log in and do some more work. It is not obvious how to sign in to the sub-account
after they are done with creating it. [Follow these instructions](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html)