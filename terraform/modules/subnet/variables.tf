variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "public_subnet_cidr" {
  description = "CIDR block of public subnet"
  type        = string
}

variable "private_subnet_cidr" {
  description = "CIDR block of private subnet"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
}