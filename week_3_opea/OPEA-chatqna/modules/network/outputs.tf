#########################################################################
# Terraform Outputs: Network Resource Identifiers
#
# These outputs provide critical identifiers for key network resources
# created by the configuration. They can be used for integration with other
# modules or for further automation tasks. Each output includes an extensive
# description explaining its role within the overall architecture.
#########################################################################

# Output for the VPC ID
output "vpc_id" {
  description = <<EOF
The unique identifier of the Virtual Private Cloud (VPC) created for this project.
This VPC serves as the foundational network container that hosts all other AWS 
resources such as subnets, instances, and security groups. This output is vital
for referencing the VPC in other modules or configurations, especially when 
establishing network connectivity or integrating with other AWS services.
EOF
  value = aws_vpc.main.id
}

# Output for the Public Subnet ID
output "public_subnet_id" {
  description = <<EOF
The identifier for the public subnet within the VPC. This subnet is specifically
configured to automatically assign public IP addresses to instances launched within
it, enabling direct communication with the internet. This output is critical for 
resources that require public access and for setting up routing and firewall rules.
EOF
  value = aws_subnet.public.id
}

# Output for the Security Group ID
output "security_group_id" {
  description = <<EOF
The unique identifier of the security group established for the deployment. This
security group governs both inbound and outbound network traffic to the associated 
resources. It plays a crucial role in ensuring that proper security measures are 
enforced, such as allowing SSH and HTTP access while restricting unauthorized connections.
EOF
  value = aws_security_group.main.id
}
