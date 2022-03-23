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

## Add ansible role to the deployment

To use WebStacks we need to install [Caktus AWS Web Stacks Role](https://github.com/caktus/ansible-role-aws-web-stacks) into the project.

Add the following to `deploy/requirements.yaml`:

```yaml
- src: https://github.com/caktus/ansible-role-aws-web-stacks
  name: caktus.aws-web-stacks
  version: ''
```

## Install the role

```shell
$ ansible-galaxy install -f -r deploy/requirements.yaml
```

## Run the CloudFormation Stack Playbook

```shell
$ ansible-playbook deploy/deploy-cf-stack.yaml
```


## The trouble with Bastion
Currently, [there is a known limitation with WebStacks and Bastion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#aws-specific-parameter-types) Even if your project
does not need a Bastion server, the cloudformation process will fail because of a Type
validation check. So a workaround is to create a key pair in EC2, and use the keyname in 
the `BastionKeyName` variable.

### Create a Key Pair
1. Navigate to EC2 in the AWS console. 
   
    **NOTE**: Make sure you are in the same region the cluster will be created in.
1. Under `Network and Security` menu on the left select `Key Pairs`
1. Click the `Create Pair` button in the top right.
1. Enter the Key name you wish to use.
1. Select `ED25519` type.
1. Click `Create Key Pair`



