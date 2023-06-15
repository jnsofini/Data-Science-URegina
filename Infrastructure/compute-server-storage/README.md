# Infrastructure

This README provides information on how to provision a basic infrastructure in AWS using Terraform. Terraform is a powerful tool for infrastructure configuration and management. To set up the infrastructure, follow the steps outlined below.

## Prerequisites

Before getting started, ensure that you have Terraform installed on your local machine. If you don't have it already, you can refer to the [official Terraform installation guide](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) for instructions tailored to your operating system.

## Description of Infrastructure

The infrastructure consists of an EC2 instance for compute and an S3 bucket for artifact storage. Refer to the diagram below for a visual representation of the infrastructure:

![Infrastructure Diagram](../images/proto-compute.webp)

_Image credit: HashiCorp_

## Requirements

To create the necessary infrastructure, you will need to perform the following tasks:

1. Create a VPC.
2. Attach an Internet Gateway to the VPC.
3. Configure a public subnet for the EC2 instance.
4. Set up a public route table.
5. Define a security group for the EC2 instance.
6. Launch an EC2 instance.
7. Verify the setup to ensure everything is functioning correctly.

Additionally, you will need to provide a bucket name for artifact storage. You can find the relevant configuration in the `iamrole_ec2_s3.tf` file on line 4. Furthermore, it's important to generate a private and public key-pair, which are necessary for SSH connectivity testing once the infrastructure is built. To generate the key-pair in Ubuntu 22.04, use the following command from the root directory of the Terraform project, `compute-server-storage`:

```bash
ssh-keygen -t rsa -b 4096 -m pem -f demo_kp && openssl rsa -in demo_kp -outform pem && chmod 400 demo_kp.pem
```

## Provisioning

To provision the infrastructure in AWS, ensure that the correct AWS profile is set. For detailed instructions on setting AWS profiles locally, refer to the AWS documentation. By default, the script assumes the use of the default profile, which is a good security practice to avoid exposing credentials. Keep in mind that this demo infrastructure has been designed for access from a single IP address. In the future, it can be modified to allow access from multiple IPs and integrate with Active Directory. Once you have added the IP address, execute the following commands:

```sh
terraform init # downloads the necessary plugins for the project
terraform plan # identifies the necessary changes, including infrastructure to be provisioned
terraform apply # deploys the services in AWS
```

To connect to the EC2 instance, use the following SSH command:

```sh
ssh -i "tutorial_kp" ubuntu@$(terraform output -raw web_public_dns)
```

If you successfully connect to the Ubuntu server, you have completed the setup process.

## Installing Tools

After connecting to the server, you may want to install additional tools. One of the necessary tools is Anaconda Python, which can be installed according to your requirements.

## Expanding Team Connectivity

To expand team connectivity beyond a single person, further configuration steps are required. This section will be updated in the future to provide detailed instructions on how to achieve this.

## Clean Up

If you are here for learning purposes and wants to destroy your infrastructure, you can simply run
`terraform apply -destroy -auto-approve`
