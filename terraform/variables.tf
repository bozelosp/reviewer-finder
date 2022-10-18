variable "aws_access_key" {
  description = "AWS pem key"
  type = string
}

variable "main_nodes_count" {
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

variable "zone"{
    description = "Availability zone"
    type = string
    default = "eu-central-1a"
}

variable "my_ip" {
  description = "My IP address"
  type = string
  default = "0.0.0.0/0"
  
}

variable "main_node_rbd" {
    description = "Root block device volume size for main nodes"
    type = number
    default = 8
}

variable "proxy_node_rbd" {
    description = "Root block device volume size for proxy node"
    type = number
    default = 200
}

variable "main_node_instance_type"{
    description = "Instance type for main nodes"
    type = string
    default = "r5a.large"
}

variable "proxy_node_instance_type"{
    description = "Instance type for proxy node"
    type = string
    default = "r5a.large"
}




