# Amazon Web Services (AWS)


## Encryption by default

Configure your AWS account to enforce the encryption of new EBS volumes and snapshots. A few notes:

* You can launch an instance only if the instance type supports EBS encryption when you enable encryption by default.
* Encryption by default is a region-specific setting.

Follow the [Encryption by default instructions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#encryption-by-default) or you can use the AWS CLI. For example:

```shell
aws --region us-west-1 ec2 enable-ebs-encryption-by-default
```
