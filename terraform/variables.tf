variable "aws_access_key" {
  description = "AWS pem key"
  type = string
}

variable "servers_count" {
  description = "Number of servers to create"
  type = number
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type = string
  default = "10.0.0.0/24"
}

variable "subnet_cidr" {
  description = "CIDR block for the subnet"
  type = string
  default = "10.0.0.0/24"
}

variable "my_ip" {
  description = "My IP address"
  type = string
  default = "0.0.0.0/0"
  
}

variable "rbd" {
    description = "Root block device volume size"
    type = number
    default = 8
}

variable "zone"{
    description = "Availability zone"
    type = string
    default = "eu-central-1a"
}
