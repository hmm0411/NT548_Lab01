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

output "igw_id" {
  description = "Internet Gateway ID"
  value       = module.subnet.igw_id
}

output "nat_gateway_id" {
  description = "NAT Gateway ID"
  value       = module.subnet.nat_gateway_id
}

output "public_route_table_id" {
  description = "Public route table ID"
  value       = module.route_table.public_route_table_id
}

output "private_route_table_id" {
  description = "Private route table ID"
  value       = module.route_table.private_route_table_id
}

output "public_sg_id" {
  description = "Public EC2 security group ID"
  value       = module.security_group.public_sg_id
}

output "private_sg_id" {
  description = "Private EC2 security group ID"
  value       = module.security_group.private_sg_id
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