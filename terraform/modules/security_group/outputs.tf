output "public_sg_id" {
  description = "Security Group ID for public EC2"
  value       = aws_security_group.public_ec2_sg.id
}

output "private_sg_id" {
  description = "Security Group ID for private EC2"
  value       = aws_security_group.private_ec2_sg.id
}