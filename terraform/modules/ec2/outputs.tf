output "public_ec2_id" {
  description = "Public EC2 instance ID"
  value       = aws_instance.public_ec2.id
}

output "private_ec2_id" {
  description = "Private EC2 instance ID"
  value       = aws_instance.private_ec2.id
}

output "public_ec2_public_ip" {
  description = "Public IP of public EC2"
  value       = aws_instance.public_ec2.public_ip
}

output "public_ec2_private_ip" {
  description = "Private IP of public EC2"
  value       = aws_instance.public_ec2.private_ip
}

output "private_ec2_private_ip" {
  description = "Private IP of private EC2"
  value       = aws_instance.private_ec2.private_ip
}