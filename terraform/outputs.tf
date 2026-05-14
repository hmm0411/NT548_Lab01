output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "public_subnet_id" {
  description = "Public subnet ID"
  value       = module.subnet.public_subnet_id
}

output "private_subnet_id" {
  description = "Private subnet ID"
  value       = module.subnet.private_subnet_id
}

output "public_ec2_public_ip" {
  description = "Public IP of public EC2"
  value       = module.ec2.public_ec2_public_ip
}

output "public_ec2_private_ip" {
  description = "Private IP of public EC2"
  value       = module.ec2.public_ec2_private_ip
}

output "private_ec2_private_ip" {
  description = "Private IP of private EC2"
  value       = module.ec2.private_ec2_private_ip
}