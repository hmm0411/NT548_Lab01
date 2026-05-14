variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "nt548-lab01"
}

variable "vpc_cidr" {
  description = "CIDR block of VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block of public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR block of private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "my_ip" {
  description = "Your public IP address for SSH access"
  type        = string
}

variable "public_key_path" {
  description = "Path to public SSH key"
  type        = string
}