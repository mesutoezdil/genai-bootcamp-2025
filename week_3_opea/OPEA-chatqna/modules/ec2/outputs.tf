output "instance_identifier" {
  description = "The unique identifier of the EC2 instance."
  value       = aws_instance.project_instance.id
}

output "instance_public_ip" {
  description = "The public IP address assigned to the EC2 instance."
  value       = aws_instance.project_instance.public_ip
}

output "instance_public_dns" {
  description = "The public DNS name of the EC2 instance."
  value       = aws_instance.project_instance.public_dns
}

output "ssh_key_pair_name" {
  description = "The name of the SSH key pair used to access the instance."
  value       = aws_key_pair.project_key.key_name
}

output "ssh_config_file_path" {
  description = "The file path to the generated SSH configuration file."
  value       = local_file.linux_ssh_config.filename
}
