#################################################################
# Terraform Variables for OPEA ChatQnA Deployment on AWS
#
# This file defines the core input parameters used to provision
# the AWS infrastructure and deploy the OPEA ChatQnA application.
# Each variable includes a detailed description to facilitate
# maintenance and customization.
#################################################################

variable "aws_region" {
  description = <<EOF
Specifies the AWS region in which the resources will be deployed.
Choose a region that is geographically close to your user base to optimize latency 
and performance. For example, "us-east-1" is widely used for deployments in the eastern US.
EOF
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  description = <<EOF
Defines the name of your project, which is used as a prefix for naming AWS resources.
This naming convention helps organize resources, making them easier to identify and manage.
For example, resources will be tagged with "opea-chatqna" to reflect their association with this project.
EOF
  type    = string
  default = "opea-chatqna"
}

variable "vpc_cidr_block" {
  description = <<EOF
Sets the CIDR block for the Virtual Private Cloud (VPC).
This IP range defines the network boundaries for all resources within the VPC.
A common setting is "10.0.0.0/16", which allows for 65,536 IP addresses.
EOF
  type    = string
  default = "10.0.0.0/16"
}

variable "instance_type" {
  description = <<EOF
Specifies the type of EC2 instance to deploy.
For the OPEA ChatQnA application, the recommended instance type is "m7i.4xlarge" to ensure 
adequate performance and compute capacity for handling AI workloads.
EOF
  type    = string
  default = "m7i.4xlarge" # Recommended instance type for OPEA ChatQnA
}

variable "ami_id" {
  description = <<EOF
Provides the Amazon Machine Image (AMI) ID to be used for launching the EC2 instance.
This AMI should correspond to Ubuntu, as specified in the OPEA documentation.
Ensure that the selected AMI is available in your chosen AWS region.
EOF
  type    = string
  default = "ami-04dd23e62ed049936" # Ubuntu as specified in OPEA docs
}

variable "ssh_public_key_path" {
  description = <<EOF
Specifies the file path to your SSH public key.
This key is used to create an AWS key pair for secure access to the instance.
Ensure the path is correct and the file exists on your local machine.
EOF
  type    = string
  default = "~/.ssh/id_rsa.pub"
}

variable "ssh_private_key_path" {
  description = <<EOF
Specifies the file path to your SSH private key.
This key is essential for generating SSH configuration and for secure remote access to the instance.
Keep this file secure and do not share it publicly.
EOF
  type    = string
  default = "~/.ssh/id_rsa"
}

variable "root_volume_size" {
  description = <<EOF
Determines the size (in GB) of the root volume attached to the EC2 instance.
A typical value for the OPEA ChatQnA deployment is 100GB, which provides sufficient 
storage for application data and logs.
EOF
  type    = number
  default = 100 # 100GB as specified in OPEA docs
}

variable "huggingface_token" {
  description = <<EOF
The API token for accessing Hugging Face models.
This token allows the ChatQnA application to retrieve and work with AI models.
Obtain your token from https://huggingface.co/settings/tokens and keep it secure.
EOF
  type      = string
  sensitive = true
}

variable "opea_release_version" {
  description = <<EOF
Specifies the release version of the OPEA application to deploy.
This version should match a valid tag in the GenAIExamples repository (e.g., "1.2").
Update this value as new versions of the application are released.
EOF
  type    = string
  default = "1.2" # Update with the latest version when available
}
