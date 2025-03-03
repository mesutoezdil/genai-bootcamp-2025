#########################################################################
# Terraform AWS Infrastructure Deployment
#
# This configuration orchestrates the setup of AWS resources by defining the
# provider and leveraging modular components. Two primary modules are used:
# 1. A network module to create the VPC, subnets, and security groups.
# 2. An EC2 module to provision instances with proper configuration and access.
#
# The configuration emphasizes reusability, clarity, and separation of concerns,
# ensuring that each module is self-contained and well-documented.
#########################################################################

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

#########################################################################
# AWS Provider Configuration
#
# The provider block initializes AWS settings, specifying the target region and
# the AWS CLI profile. The region is dynamically determined from a variable,
# which allows for flexible deployments across different AWS regions.
#########################################################################
provider "aws" {
  region  = var.aws_region
  profile = "sunbirdai"   # Ensure this profile is set up in your AWS CLI configuration.
}

#########################################################################
# Module: Network Infrastructure
#
# This module is responsible for provisioning the core network resources:
# - Virtual Private Cloud (VPC) with a defined CIDR block.
# - Public Subnet for resources requiring direct internet access.
# - Security components such as Internet Gateway and security groups.
#
# Input Variables:
#   - project_name: Prefix for naming resources.
#   - vpc_cidr_block: Defines the IP address range for the VPC.
#   - aws_region: Specifies the region for resource deployment.
#########################################################################
module "network" {
  source = "./modules/network"

  project_name   = var.project_name
  vpc_cidr_block = var.vpc_cidr_block
  aws_region     = var.aws_region
}

#########################################################################
# Module: EC2 Instance Provisioning
#
# The EC2 module deploys compute instances within the network created above.
# It integrates with the network module to ensure instances are placed in the
# appropriate subnet and secured by the correct security groups.
#
# Key configuration details include:
#   - Instance type and AMI for hardware and operating system specifications.
#   - SSH key paths for secure, key-based authentication.
#   - Root volume size for instance storage.
#   - Application-specific parameters such as the Hugging Face token and
#     the application release version.
#   - Host operating system configuration for correct execution of local scripts.
#########################################################################
module "ec2" {
  source = "./modules/ec2"

  project_name         = var.project_name
  instance_type        = var.instance_type        # e.g., t3.medium, m5.large, etc.
  ami_id               = var.ami_id               # The AMI identifier for launching instances.
  subnet_id            = module.network.public_subnet_id
  security_group_id    = module.network.security_group_id
  ssh_public_key_path  = var.ssh_public_key_path    # Path to the SSH public key.
  ssh_private_key_path = var.ssh_private_key_path   # Path to the SSH private key.
  root_volume_size     = var.root_volume_size       # Disk size (in GB) for the root volume.
  huggingface_token    = var.huggingface_token      # Token for accessing Hugging Face services.
  opea_release_version = var.opea_release_version   # Version tag for the deployed application.
  host_os              = "linux"                    # Defines the host OS, influencing script interpreters.
}
