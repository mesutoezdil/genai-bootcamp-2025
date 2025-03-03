#########################################################################
# Terraform Outputs: EC2 Instance & ChatQnA Access Details
#
# This section outputs essential details for accessing the deployed 
# ChatQnA application and its underlying EC2 instance. Use these outputs
# to quickly connect via SSH, access the web application, and review 
# initialization logs.
#########################################################################

output "instance_public_ip" {
  description = <<EOF
The public IP address of the EC2 instance hosting the ChatQnA application.
This IP is used for web access and secure SSH connections.
EOF
  value = module.ec2.public_ip
}

output "chatqna_access_url" {
  description = <<EOF
The URL to access the ChatQnA application. It combines the instance's public IP 
with port 80. Open this URL in your browser to interact with the ChatQnA service.
EOF
  value = "http://${module.ec2.public_ip}:80"
}

output "instance_ssh_command" {
  description = <<EOF
The SSH command to log in to the EC2 instance. Make sure the SSH private key 
specified in the variable is accessible on your machine.
EOF
  value = "ssh -i ${var.ssh_private_key_path} ubuntu@${module.ec2.public_ip}"
}

output "generated_ssh_config_file" {
  description = <<EOF
The path to the automatically generated SSH configuration file. This file contains 
preconfigured settings to simplify the process of connecting to your EC2 instance.
EOF
  value = module.ec2.ssh_config_file
}

output "ssh_config_usage_instructions" {
  description = <<EOF
Instructions for applying the generated SSH configuration. To load the configuration 
into your SSH client, execute the following command in your terminal:

cat ${module.ec2.ssh_config_file} | bash
EOF
  value = "To apply the SSH configuration, run: cat ${module.ec2.ssh_config_file} | bash"
}

output "cloud_init_log_command" {
  description = <<EOF
Command to view the cloud-init logs on the EC2 instance. These logs help verify that 
all initialization scripts ran successfully during instance startup.
EOF
  value = "ssh -i ${var.ssh_private_key_path} ubuntu@${module.ec2.public_ip} 'sudo cat /var/log/cloud-init-output.log'"
}
