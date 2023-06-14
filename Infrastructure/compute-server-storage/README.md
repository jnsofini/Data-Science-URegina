# Infrastructure

We want to provision a basic infrastructure in AWS to act as a starting point for a small team to develop models. The method choice is [`Terraform`](https://developer.hashicorp.com/terraform/intro) which is a great tool for infrastructure configuration and management. We will use Terraform to deploy resources as inpired by [Matt Little](https://medium.com/@TheMattLittle) in this [Medium article](https://medium.com/strategio/using-terraform-to-create-aws-vpc-ec2-and-rds-instances-c7f3aa416133). First setup terraform locally by checking [`this link`](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) and following the instruction for your OS.  With terraform installed:

## Description of Infrastructure

The infrastructure contains mainly of and EC2 for compute and an S3 for artifact storage. A simple sketch of the infrastructure is as follows.

![Image credit HashiCorp](../images/proto-compute.webp) _Image credit HashiCorp_

## Requirement

To accomplish these tasks for the team we will need to create

- VPC
- Internet Gateway and attach it to the VPC
- subnets: 1 public for EC2
- public route table
- security group for EC2
- EC2 instance
- Verify that everything is set up correctly

The terraform code provided can build an insfratucture with a small compute for demo purposes. Also, a bucket name must be provided, see line 4 of `iamrole_ec2_s3.tf`. The code expects that we have a private and public key-pair. They SSH keys are necessary to test connectivity once the insfratcture is built. To generate the key-pair we use the following in Ubuntu 22.04. Create the Key Pair in the terraform project root directory `compute-server-storage` via the following command:

```bash
ssh-keygen -t rsa -b 4096 -m pem -f demo_kp && openssl rsa -in demo_kp -outform pem && chmod 400 demo_kp.pem
```

## Provision

To get the insfrastructure in aws, ensure the right profile has been set. For more details on setting AWS profiles locally consult ???. Here we are assuming the default profile. See line 22 of `main.tf`. Profiles are encouraged to avaoid exposing credentials. This is a good security practice. This demo infrastructure was also build for access from a single IP address. In the future we will open it to multiple IPs and also demo access from Active Directory. After adding the IP address, run the following

```sh
terraform init # downloads the necessary plugins for the project
terraform plan # identify the neccerary changes including infra to provision
terraform apply # deploy the services in AWS
```

To connect to the instance use

```sh
ssh -i "tutorial_kp" ubuntu@$(terraform output -raw web_public_dns)
```

If you are in the ubuntu server then you have a success story.

## Installing tools

Some of the tools neccessary includes Anaconda Python which can be installed.

## Connecting to Server

TODO: Explain how to expand the team connectivity beyond one person