variable "project_name" {
  description = "Project name"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID"
  type        = string
}

variable "private_subnet_id" {
  description = "Private subnet ID"
  type        = string
}

variable "public_sg_id" {
  description = "Security Group ID for public EC2"
  type        = string
}

variable "private_sg_id" {
  description = "Security Group ID for private EC2"
  type        = string
}

variable "public_key_path" {
  description = "Path to public SSH key"
  type        = string
}