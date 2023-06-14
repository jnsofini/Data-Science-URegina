// Here is where we are defining
// our Terraform settings
terraform {
  required_providers {
    // The only required provider we need
    // is aws, and we want version 4.0.0
    aws = {
      source  = "hashicorp/aws"
      version = "4.0.0"
    }
  }

  // This is the required version of Terraform
  required_version = "~> 1.4"
}

// Here we are configuring our aws provider. 
// We are setting the region to the region of 
// our variable "aws_region"
provider "aws" {
  region = var.aws_region
  profile = "default"
}

// Set some variables
locals {
  name    = "ml-dev-server"
  region  = "us-west-2"

  //vpc_cidr = "10.0.0.0/16"
  //azs      = slice(data.aws_availability_zones.available.names, 0, 3)

  tags = {
    Name       = local.name
    Environment    = local.name
  }
}

// This data object is going to be
// holding all the available availability
// zones in our defined region
data "aws_availability_zones" "available" {
  state = "available"
}

// 2. AMI
// Create a data object called "ubuntu" that holds the latest
// Ubuntu 20.04 server AMI
data "aws_ami" "ubuntu" {
  // We want the most recent AMI
  most_recent = "true"

  // We are filtering through the names of the AMIs. We want the 
  // Ubuntu 20.04 server
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  // We are filtering through the virtualization type to make sure
  // we only find AMIs with a virtualization type of hvm
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  
  // This is the ID of the publisher that created the AMI. 
  // The publisher of Ubuntu 20.04 LTS Focal is Canonical 
  // and their ID is 099720109477
  owners = ["099720109477"]
}

// 3. VPC
// Create a VPC named "ml_vpc"
resource "aws_vpc" "ml_vpc" {
  // Here we are setting the CIDR block of the VPC
  // to the "vpc_cidr_block" variable
  cidr_block           = var.vpc_cidr_block
  // We want DNS hostnames enabled for this VPC
  enable_dns_hostnames = true

  // We are tagging the VPC with the name "ml_vpc"
  tags = {
    Name = "ml_vpc"
  }
}

// 4. Internet GateWay
// Create an internet gateway named "ml_igw"
// and attach it to the "ml_vpc" VPC
resource "aws_internet_gateway" "ml_igw" {
  // Here we are attaching the IGW to the 
  // ml_vpc VPC
  vpc_id = aws_vpc.ml_vpc.id

  // We are tagging the IGW with the name ml_igw
  tags = {
    Name = "ml_igw"
  }
}

// 5. Public Subnet
// Create a group of public subnets based on the variable subnet_count.public
resource "aws_subnet" "ml_public_subnet" {
  // count is the number of resources we want to create
  // here we are referencing the subnet_count.public variable which
  // current assigned to 1 so only 1 public subnet will be created
  count             = var.subnet_count.public
  
  // Put the subnet into the "ml_vpc" VPC
  vpc_id            = aws_vpc.ml_vpc.id
  
  // We are grabbing a CIDR block from the "public_subnet_cidr_blocks" variable
  // since it is a list, we need to grab the element based on count,
  // since count is 1, we will be grabbing the first cidr block 
  // which is going to be 10.0.1.0/24
  cidr_block        = var.public_subnet_cidr_blocks[count.index]
  
  // We are grabbing the availability zone from the data object we created earlier
  // Since this is a list, we are grabbing the name of the element based on count,
  // so since count is 1, and our region is us-east-2, this should grab us-east-2a
  availability_zone = data.aws_availability_zones.available.names[count.index]

  // We are tagging the subnet with a name of "ml_public_subnet_" and
  // suffixed with the count
  tags = {
    Name = "ml_public_subnet_${count.index}"
  }
}


// 5. Public Route table
// Create a public route table named "ml_public_rt"
resource "aws_route_table" "ml_public_rt" {
  // Put the route table in the "ml_vpc" VPC
  vpc_id = aws_vpc.ml_vpc.id

  // Since this is the public route table, it will need
  // access to the internet. So we are adding a route with
  // a destination of 0.0.0.0/0 and targeting the Internet 	 
  // Gateway "ml_igw"
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.ml_igw.id
  }
}

// 6. Routable association
// Here we are going to add the public subnets to the 
// "ml_public_rt" route table
resource "aws_route_table_association" "public" {
  // count is the number of subnets we want to associate with
  // this route table. We are using the subnet_count.public variable
  // which is currently 1, so we will be adding the 1 public subnet
  count          = var.subnet_count.public
  
  // Here we are making sure that the route table is
  // "ml_public_rt" from above
  route_table_id = aws_route_table.ml_public_rt.id
  
  // This is the subnet ID. Since the "ml_public_subnet" is a 
  // list of the public subnets, we need to use count to grab the
  // subnet element and then grab the id of that subnet
  subnet_id      = 	aws_subnet.ml_public_subnet[count.index].id
}




// 9. SG ec2
// Create a security for the EC2 instances called "ml_web_sg"
resource "aws_security_group" "ml_web_sg" {
  // Basic details like the name and description of the SG
  name        = "ml_web_sg"
  description = "Security group for ml web servers"
  // We want the SG to be in the "ml_vpc" VPC
  vpc_id      = aws_vpc.ml_vpc.id

  // The first requirement we need to meet is "EC2 instances should 
  // be accessible anywhere on the internet via HTTP." So we will 
  // create an inbound rule that allows all traffic through
  // TCP port 80.
  ingress {
    description = "Allow all traffic through HTTP"
    from_port   = "80"
    to_port     = "80"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  // The second requirement we need to meet is "Only you should be 
  // "able to access the EC2 instances via SSH." So we will create an 
  // inbound rule that allows SSH traffic ONLY from your IP address
  ingress {
    description = "Allow SSH from my computer"
    from_port   = "22"
    to_port     = "22"
    protocol    = "tcp"
    // This is using the variable "my_ip"
    cidr_blocks = ["${var.my_ip}/32"]
  }

  // This outbound rule is allowing all outbound traffic
  // with the EC2 instances
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  // Here we are tagging the SG with the name "ml_web_sg"
  tags = {
    Name = "ml_web_sg"
  }
}


// 13. Key-Pair
// Create a key pair named "ml_kp"
resource "aws_key_pair" "ml_kp" {
  // Give the key pair a name
  key_name   = "ml_kp"
  
  // This is going to be the public key of our
  // ssh key. The file directive grabs the file
  // from a specific path. Since the public key
  // was created in the same directory as main.tf
  // we can just put the name
  # public_key = file("/home/fini/.ssh/ml_rsa.pub")
  public_key = file("ml_kp.pub")
}

// 14. EC2
// Create an EC2 instance named "ml_web"
resource "aws_instance" "ml_web" {
  // count is the number of instance we want
  // since the variable settings.web_app.cont is set to 1, we will only get 1 EC2
  count                  = var.settings.web_app.count
  
  // Here we need to select the ami for the EC2. We are going to use the
  // ami data object we created called ubuntu, which is grabbing the latest
  // Ubuntu 20.04 ami
  // Changed to see if we can get linux to work
  ami                    = var.linux_ami #data.aws_ami.ubuntu.id
  
  // This is the instance type of the EC2 instance. The variable
  // settings.web_app.instance_type is set to "t2.micro"
  instance_type          = var.settings.web_app.instance_type
  
  // The subnet ID for the EC2 instance. Since "ml_public_subnet" is a list
  // of public subnets, we want to grab the element based on the count variable.
  // Since count is 1, we will be grabbing the first subnet in  	
  // "ml_public_subnet" and putting the EC2 instance in there
  subnet_id              = aws_subnet.ml_public_subnet[count.index].id
  
  // The key pair to connect to the EC2 instance. We are using the "ml_kp" key 
  // pair that we created
  key_name               = aws_key_pair.ml_kp.key_name
  
  // The security groups of the EC2 instance. This takes a list, however we only
  // have 1 security group for the EC2 instances.
  vpc_security_group_ids = [aws_security_group.ml_web_sg.id]

  // Attached role to access s3 bucket
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name

  // We want to setup mlflow server in it. So lets put the user data
  user_data = "${file("init.sh")}"

  // We are tagging the EC2 instance with the name "ml_web" followed by
  // the count index
  tags = {
    Name = "ml_web_${count.index}"
  }
}

// 15. EIP
// Create an Elastic IP named "ml_web_eip" for each
// EC2 instance
resource "aws_eip" "ml_web_eip" {
	// count is the number of Elastic IPs to create. It is
	// being set to the variable settings.web_app.count which
	// refers to the number of EC2 instances. We want an
	// Elastic IP for every EC2 instance
  count    = var.settings.web_app.count

	// The EC2 instance. Since ml_web is a list of 
	// EC2 instances, we need to grab the instance by the 
	// count index. Since the count is set to 1, it is
	// going to grab the first and only EC2 instance
  instance = aws_instance.ml_web[count.index].id

	// We want the Elastic IP to be in the VPC
  vpc      = true

	// Here we are tagging the Elastic IP with the name
	// "ml_web_eip_" followed by the count index
  tags = {
    Name = "ml_web_eip_${count.index}"
  }
}


