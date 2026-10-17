# GroceryMate Infrastructure as Code

## Verification status

Terraform formatting and validation have passed locally.
The existing AWS deployment was created manually.
Existing resources have not been imported into this Terraform state.
The new EC2 bootstrap has not been tested on a newly provisioned instance.

Validation checks configuration consistency, not successful deployment.

## Infrastructure

- Amazon Linux EC2 with encrypted root storage and IMDSv2
- Application and database Security Groups
- Private PostgreSQL RDS with encrypted storage
- RDS-managed master credentials in Secrets Manager
- Private encrypted S3 avatar bucket
- EC2 IAM role with access to its database secret and avatar bucket
- Docker application startup through user_data and systemd

## Local validation

Run from the repository root:

    terraform -chdir=infrastructure init -backend=false
    terraform -chdir=infrastructure fmt -check
    terraform -chdir=infrastructure validate

## Configuration

Copy terraform.tfvars.example to terraform.tfvars.
Replace all placeholders locally.

app_revision must contain the full SHA of a pushed Git commit that
includes the application Secrets Manager integration.

Obtain the SHA after committing and pushing:

    git rev-parse HEAD

Set s3_bucket_name explicitly.
Choose a final_snapshot_identifier that does not already exist.
Never commit credentials, local variable files, state or saved plans.

## Password handling

RDS manages the master password in Secrets Manager.
Terraform does not supply the master password.

The application retrieves credentials at worker startup through its
EC2 IAM role. The runtime configuration contains the secret ARN,
not the database password.

Automatic credential refresh after rotation is not implemented.
Application workers may need to be restarted after password rotation.

Coordinate any transition of the existing database to managed
credentials with the application deployment.

Do not retrieve secret values through Terraform merely to insert
passwords into user_data or environment files.

## State protection

The configuration currently uses local state.
A protected remote backend has not been configured.

Managed RDS credentials remove the need to supply the master password
to Terraform. State still contains infrastructure information.
Protect the workstation and state backups.
Do not commit state or paste its contents into chat.

## Discover existing resources

Confirm account and region before importing:

    aws sts get-caller-identity

Inspect EC2:

    aws ec2 describe-instances --region eu-central-1 --query "Reservations[].Instances[].{Id:InstanceId,Subnet:SubnetId,Groups:SecurityGroups,Profile:IamInstanceProfile.Arn}" --output json

Inspect RDS:

    aws rds describe-db-instances --region eu-central-1 --query "DBInstances[].{Id:DBInstanceIdentifier,SubnetGroup:DBSubnetGroup.DBSubnetGroupName,Groups:VpcSecurityGroups,Engine:EngineVersion,Storage:AllocatedStorage,Encrypted:StorageEncrypted}" --output json

Match the configuration to the real resources before applying changes.

The generated database identifier currently differs from database-1.
Review names, AMI, subnet, root disk, encryption, database settings,
IAM policies and all Security Group rules.

The existing EC2 uses multiple Security Groups. Do not assume that
either group is an exact match for aws_security_group.application.

The existing load balancer and target group are outside this configuration.

## Import procedure

Import records existing resources in Terraform state.
It does not make the configuration match their deployed settings.

First configure all required variables and initialize Terraform:

    terraform -chdir=infrastructure init

Only run the following examples after verifying resource ownership,
identifiers and the intended Terraform address.

Verify these original identifiers in AWS before using them:

    terraform -chdir=infrastructure import aws_instance.application i-0d3f05f49de3c67b1
    terraform -chdir=infrastructure import aws_db_instance.database database-1

For the bucket, replace EXISTING_BUCKET with its verified name:

    terraform -chdir=infrastructure import aws_s3_bucket.avatars EXISTING_BUCKET
    terraform -chdir=infrastructure import aws_s3_bucket_public_access_block.avatars EXISTING_BUCKET
    terraform -chdir=infrastructure import aws_s3_bucket_server_side_encryption_configuration.avatars EXISTING_BUCKET

For Security Groups, replace each placeholder with its verified ID:

    terraform -chdir=infrastructure import aws_security_group.application sg-APPLICATION
    terraform -chdir=infrastructure import aws_security_group.database sg-DATABASE

Import the existing database subnet group:

    terraform -chdir=infrastructure import aws_db_subnet_group.database EXISTING_SUBNET_GROUP

Import the existing IAM role and instance profile:

    terraform -chdir=infrastructure import aws_iam_role.ec2 EXISTING_ROLE
    terraform -chdir=infrastructure import aws_iam_instance_profile.ec2 EXISTING_PROFILE

An inline role policy uses ROLE_NAME:POLICY_NAME:

    terraform -chdir=infrastructure import aws_iam_role_policy.s3_access EXISTING_ROLE:EXISTING_INLINE_POLICY

Do not import an attached managed policy as an inline policy.
If the matching resource does not exist, record it as a proposed creation.
The new rds_secret inline policy may not have an existing equivalent.

VPC, subnet and AMI data sources are read automatically.
They are not imported.

## Review after import

    terraform -chdir=infrastructure state list
    terraform -chdir=infrastructure plan

Review every creation, update, replacement and deletion.
Resolve configuration differences before applying the plan.

Do not replace or delete the existing deployment merely to make it
match this configuration.

## EC2 bootstrap

user_data.sh.tftpl installs Docker, clones the configured repository,
checks out a pinned Git commit, builds the backend image and starts
grocerymate-container.service.

The container uses host networking to access instance role credentials
through IMDSv2.

The JWT secret is generated on the instance.
Local environment files are excluded from the Docker build context.

The application currently downloads the frontend from the original
course repository's latest release. This artifact is not pinned.

The bootstrap does not restore database tables or course data.
A fresh database requires a separate schema and data migration.

The homepage readiness check does not verify database contents.
Check the product API separately after provisioning.

Changing user_data on an existing instance is not a verified
in-place application deployment procedure. The first-boot script
must not be assumed to run again automatically.

## Runtime verification

On a newly provisioned EC2 instance:

    sudo cloud-init status --long
    sudo systemctl status grocerymate-container --no-pager
    sudo journalctl -u grocerymate-container -n 50 --no-pager
    curl --fail http://127.0.0.1:5000/api/products/all_products

Review logs locally before sharing them.
A successful product request requires the schema and data to exist.

## Database protection

Terraform prevent_destroy and RDS deletion_protection are enabled.
Automated backups use backup_retention_days.
A deliberately permitted future deletion must create a final snapshot.

These settings do not replace a tested backup and restore procedure.
