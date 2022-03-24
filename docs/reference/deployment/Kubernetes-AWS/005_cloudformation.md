# Cloudformation Setup

## Get the template

From the [Caktus AWS WebStacks repository](https://github.com/caktus/aws-web-stacks) find the 
template that suits your needs. For the vast majority of cases you will want to use 
[eks-nat.yaml](https://s3.amazonaws.com/aws-web-stacks/eks-nat.yaml). After downloading 
it is a good idea to set the version (e.g. `eks-nat-2.1.2.yaml`). You can grab that from the [latest tag](https://github.com/caktus/aws-web-stacks/tags).

Copy the file into your project's `deploy/stack` folder.


## Configure the ansible variables

The variables for your stack are often found in the `deploy/group_vars/all.yaml`.


EXAMPLE:

```yaml
# ----------------------------------------------------------------------------
# AWS Web Stacks: Configuration variables to be used by the
#                 caktus/aws-web-stacks role
# ----------------------------------------------------------------------------

cloudformation_stack_profile: '{{ aws_profile }}'
cloudformation_stack_region: '{{ aws_region }}'
cloudformation_stack_name: '{{ app_name }}-{{ env_name }}-stack'
cloudformation_stack_template_local_path: '{{ playbook_dir + "/stack/eks-nat-2.1.2.yaml" }}'
cloudformation_stack_template_bucket: 'aws-web-stacks-{{ app_name }}'
cloudformation_stack_template_bucket_path: 'templates/{{ env_name }}/{{ cloudformation_stack_name }}.yml'
cloudformation_stack_create_changeset: true
cloudformation_stack_template_parameters:
  PrimaryAZ: "{{ aws_region }}a"
  SecondaryAZ: "{{ aws_region }}b"
  DesiredScale: 2
  MaxScale: 2
  UseAES256Encryption: "true"
  CustomerManagedCmkArn: ""
  ContainerInstanceType: t3a.medium
  ContainerVolumeSize: 30
  DatabaseClass: db.t3.small
  DatabaseEngineVersion: "14"
  DatabaseParameterGroupFamily: postgres14
  DatabaseMultiAZ: "true"
  DatabaseUser: "{{ admin_database_user|default(app_name) }}"
  DatabasePassword: "{{ admin_database_password }}"
  DatabaseName: "{{ admin_database_name|default(app_name) }}"
  DomainName: "{{ app_name }}." ## What should this be
  DomainNameAlternates: ""
  AssetsUseCloudFront: "false"
  # Bastion host
  BastionKeyName: <some-pre-existing-key-pair>

```

**Note**: You may ask yourself, what is going on with that `BastionKeyName` variable, I don't need a bastion server. That
may be true but head to the appendix to find out why it is needed. [The Trouble With Bastion](#the-trouble-with-bastion)

**Note**: If you need to encrypt cluster secrets follow head on down to [Envelope encryption](#envelope-encryption-of-cluster-secrets)

## Add ansible role to the deployment

To use WebStacks we need to install [Caktus AWS Web Stacks Role](https://github.com/caktus/ansible-role-aws-web-stacks) into the project.

Add the following to `deploy/requirements.yaml`:

```yaml
- src: https://github.com/caktus/ansible-role-aws-web-stacks
  name: caktus.aws-web-stacks
  version: ''
```

### Install the role

```shell
$ ansible-galaxy install -f -r deploy/requirements.yaml
```

### Run the CloudFormation Stack Playbook

```shell
$ ansible-playbook deploy/deploy-cf-stack.yaml
```

## Configure Services

After cloudformation has run, it will have created a bunch of services within the AWS account.

1. An EKS cluster.
2. An ECR repository.
3. An RDS database.


## Appendix

### The trouble with Bastion
Currently, [there is a known limitation with WebStacks and Bastion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#aws-specific-parameter-types) Even if your project
does not need a Bastion server, the cloudformation process will fail because of a Type
validation check. So a workaround is to create a key pair in EC2, and use the keyname in 
the `BastionKeyName` variable.

## Create a Key Pair
1. Navigate to EC2 in the AWS console. 
   
    **NOTE**: Make sure you are in the same region the cluster will be created in.
1. Under `Network and Security` menu on the left select `Key Pairs`
1. Click the `Create Pair` button in the top right.
1. Enter the Key name you wish to use.
1. Select `ED25519` type.
1. Click `Create Key Pair`

### Envelope Encryption of Cluster Secrets

One of the considerations for the security of the cluster is whether you want to encrypt the Cluster secrets. The
decision-making process for this is well beyond the scope of this doc, but if you do, you will need to add a 
`Customer Managed Key` to the account.

1. In the AWS console, navigate to `Key Management Service (KMS)`.
1. In the top right click `Add a Key`.
1. Leave `Symmetric` checked and click `Next`.
1. Add an `Alias` for the CMK, and click `Next`.
1. 

