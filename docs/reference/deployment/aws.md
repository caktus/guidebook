# Amazon Web Services (AWS)

## Encryption by default

Configure your AWS account to enforce the encryption of new EBS volumes and snapshots. A few notes:

* You can launch an instance only if the instance type supports EBS encryption when you enable encryption by default.
* Encryption by default is a region-specific setting.

Follow the [Encryption by default instructions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#encryption-by-default) or you can use the AWS CLI. For example:

```shell
aws --region us-west-1 ec2 enable-ebs-encryption-by-default
```

## New Kubernetes Cluster

### Setting up a Client sub account

If a client needs to have a sub account created for us to use with our assume roles. Follow these instructions.

[First create the sub-account from the organizations root account](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_create.html)

Once that is done they will need to log in and do some more work. It is not obvious how to sign in to the sub-account
after they are done with creating it. [Follow these instructions](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html)

### Create an ansible vault secret

1. From the AWS console navigate to the `AWS secrets manager`
1. Click `Store a new secret`
1. Select `Other type of secret`
1. Select `Plaintext`
1. Remove the dictionary.
1. Generate a secret key from the command line `pwgen -n 64`
1. Copy one of the keys into the plaintext input. Ensure that the key is the only string present
1. Ensure that `Encryption key` has `aws/secretsmanager` selected
1. Click `Next`
1. Give your secret a name. Convention is `<projectname>-ansible-vault-secret`
1. Click `Next`
1. Click `Next` again.

### Choose versions and instance types

#### PostgreSQL RDS

Choose the latest version of PostgreSQL RDS [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts.General.DBVersions). You can also run:

```shell
aws rds describe-db-engine-versions --default-only --engine postgres
```
