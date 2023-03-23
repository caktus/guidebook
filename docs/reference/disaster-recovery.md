# Disaster Recovery

Caktus provides managed hosting services for many projects, which include periodic backups and application recovery. For example, restoring a deployed environment after (1) a hardware or cloud environment failure or (2) a user or application bug accidentally deletes data. Here we document our strategy and approach for disaster recovery.

## Our goals

* **Redundancy:** We back up or replicate data (database, uploaded files, etc.) to a separate location or region from the deployed environment. For example, if the site is deployed to `us-east-1`, backup data to `us-east-2`.
* **Recoverability:** We perform periodic backup verifications to ensure the integrity of our backups by restoring them to a freshly deployed environment.
* **Not Staging:** Backups are restored to a dedicated environment to not impact active development on staging and production.

## Prerequisites

To get started, make sure you have:

* :fontawesome-brands-aws: Caktus AWS account and AWS Command Line Interface (AWS CLI) [configured for your development projects](../developer-onboarding/AWS.md).

## Backup verification workflow

A project's documentation contains the canonical backup instructions. Please refer to your project docs for detailed setup instructions.

However, most projects should roughly follow this pattern:

1. Obtain latest production backup archive:
   ```sh
   inv utils.get-db-backup
   ```
2. Restore database archive into disaster recovery environment:
   ```sh
   inv dr deploy.db-restore --filename=<FILENAME>
   ```
3. Deploy a recent application image to the disaster recovery environment:
   ```sh
   # Find current deployed tag
   kubectl -n <NAMESPACE> get deployments -o wide
   # Deploy
   inv dr deploy --tag=<TAG>
   ```
4. Visit deployed site in your browser, log in, update Site object, and perform basic smoke tests:
    * Create new pages
    * Upload images
5. Once complete, turn off disaster recovery environment:
   ```sh
   kubectl -n <NAMESPACE> scale deployments --replicas=0 --all
   ```

## Initial setup

### DR provisioning

#### AWS - Replicated object bucket

1. Create a new bucket in the [AWS S3 console](https://s3.console.aws.amazon.com/s3/bucket/create) with:
    * **Bucket name:** `PROJECTNAME`-dr-assets
    * **AWS Region:** A region other than the source bucket for Cross-Region Replication
    * **Object Ownership:** Same as the source bucket (most likely **ACLs enabled**)
    * **Block Public Access settings for this bucket:** Same as the source bucket
    * **Bucket Versioning:** Same as the source bucket
    * **Default encryption:** Same as the source bucket
2. In the [AWS S3 console](https://s3.console.aws.amazon.com/s3/buckets), navigate to the source bucket, click the Management tab, and then select Create replication rule: 
    * **Replication rule name:** DR Replication
    * **Destination:** Select the bucket you created above
    * **IAM Role:** Select Create new role
3. After clicking Save, choose to replicate existing objects on the modal window:
    * **Completion report:** s3://`PROJECTNAME`-dr-assets/replication-reports
    * **Permissions:** Choose from existing IAM roles and Create a new role

#### Add DNS Record

Create a CNAME record, for example dr.`PROJECTNAME`.com and point it to the cluster Load Balancer DNS name or alias. 

#### Create `dr` Ansible configuration

1. Create `group_vars/staging_shared.yaml` with common configuration between `staging` and `dr`
2. Create `host_vars/dr.yaml` with domain name, basic auth password, etc.

#### Update IAM assets management policy
1. Go to IAM > Roles > and search for the  `ContainerInstanceRole`
2. Edit the AssetsManagementPolicy to include the newly-created DR bucket
    ```json
        {
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::BUCKETNAME",
            "Effect": "Allow"
        },
        {
            "Action": [
                "s3:*"
            ],
            "Resource": "arn:aws:s3:::BUCKETNAME/*",
            "Effect": "Allow"
        }
    ```

### Database backups

#### AWS - Hosting Services bucket

This private bucket will store database archives.

1. Create a new bucket in the [AWS S3 console](https://s3.console.aws.amazon.com/s3/bucket/create) with:
    * **Bucket name:** `PROJECTNAME`-hosting-services
    * **AWS Region:** A region other than the source bucket for Cross-Region Replication
    * **Object Ownership:** ACLs disabled
    * **Block Public Access settings for this bucket:** Block all public access
    * **Bucket Versioning:** Enable
    * **Default encryption:** Enable

#### Backup user

1. Create a new user in the [AWS IAM console](https://us-east-1.console.aws.amazon.com/iam/home#/users$new?step=details) with:
    *  **User name:** `PROJECTNAME`-backups
    *  **AWS credential type:** Access key - Programmatic access
    *  **Permissions:** Skip for now
    *  **Tags:** Skip for now
    *  Download and save the access credentials CSV file.
2. Click on the newly created user in the [AWS IAM console](https://us-east-1.console.aws.amazon.com/iamv2/home#/users) and click **Add inline policy**:
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "ListObjectsInBucket",
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::PROJECTNAME-hosting-services"
                ]
            },
            {
                "Sid": "ObjectActions",
                "Effect": "Allow",
                "Action": "s3:PutObject",
                "Resource": [
                    "arn:aws:s3:::PROJECTNAME-hosting-services/*"
                ]
            }
        ]
    }
    ```
