terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
}

provider "aws" {
  region  = "eu-central-1"
}


# Create a security group
resource "aws_security_group" "main" {
  name = "Main Security Group"
  description = "Allow web traffic"
  vpc_id = aws_vpc.main.id


  ingress {
    description      = "Full subnet communication"
    from_port        = 0
    to_port          = 0
    protocol         = "all"
    self             = true
    }
    
    ingress {
    description      = "SSH from my ip"
    cidr_blocks      = [var.my_ip]
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    }

    ingress {
    description      = "to Milvus port from my ip"
    cidr_blocks      = [var.my_ip]
    from_port        = 19530
    to_port          = 19530
    protocol         = "tcp"
    }

  egress {
    from_port        = 0 # 0 means all ports
    to_port          = 0 # 0 means all ports
    protocol         = "-1" # -1 means all protocols"
    cidr_blocks      = ["0.0.0.0/0"] # All ip addresses
    ipv6_cidr_blocks = ["::/0"] # All ipv6 addresses
  }

  tags = {
    Name = "Main Security Group"
  }
}


# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  
  tags = {
    Name = "Main VPC"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "Main Internet Gateway"
  }
  
}


# Create a subnet
resource "aws_subnet" "main" {
  vpc_id = aws_vpc.main.id
  cidr_block = var.subnet_cidr
  map_public_ip_on_launch = true
  availability_zone = var.zone

  tags = {
    Name = "Main Subnet"
  }
  
}


#Create a Route Table
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0" # all traffic going to gateway
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "Main Route Table"
  }
  
}


# Associate the route table with the subnet
resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}


# Create an instance
resource "aws_instance" "main_node" {
  count         = var.servers_count
  ami           = "ami-0caef02b518350c8b"
  instance_type = "r5a.large"
  key_name      = var.aws_access_key
  subnet_id     = aws_subnet.main.id
  availability_zone = var.zone
  vpc_security_group_ids = [aws_security_group.main.id]

  root_block_device {
    volume_type = "gp2"
    volume_size = var.rbd
  }

  tags = {
    Name = "Main Server ${count.index + 1}"
  }
}

resource "aws_instance" "proxy_node" {
  count         = 1
  ami           = "ami-0caef02b518350c8b"
  instance_type = "r5a.large"
  key_name      = var.aws_access_key
  subnet_id     = aws_subnet.main.id
  availability_zone = var.zone
  vpc_security_group_ids = [aws_security_group.main.id]

  root_block_device {
    volume_type = "gp2"
    volume_size = 50
  }
  tags = {
    Name = "Proxy Server"
  }
}