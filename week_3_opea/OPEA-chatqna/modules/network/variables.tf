#########################################################################
# Terraform Variables: AWS Project Configuration
#
# This section defines the key input parameters that control the naming
# conventions, network configuration, and deployment region for the AWS
# infrastructure. Detailed descriptions and examples are provided to guide
# users in setting appropriate values.
#########################################################################

variable "project_name" {
  description = <<EOF
The name of your project, which is used as a prefix to uniquely identify and
organize all AWS resources associated with this deployment. By standardizing
resource names, it becomes easier to manage and track resources across your
AWS account.

Example:
  If your project_name is "ChatQnA", resources might be named as "ChatQnA-vpc",
  "ChatQnA-sg", etc.
EOF
  type = string
}

variable "vpc_cidr_block" {
  description = <<EOF
Defines the IP address range for the Virtual Private Cloud (VPC) in CIDR notation.
This value is critical for establishing the network boundaries and ensuring proper
segmentation of the deployed infrastructure. The chosen CIDR block should provide
enough IP addresses for all anticipated resources.

Example:
  A common value is "10.0.0.0/16", which allows for 65,536 IP addresses.
EOF
  type = string
}

variable "aws_region" {
  description = <<EOF
Specifies the AWS region where your resources will be deployed. The region you
choose can affect service availability, network latency, and overall costs. By
default, this is set to "us-east-1", which is one of AWS's primary and widely used
regions. Change this value if your project requires deployment to another region,
such as "us-west-2" or "eu-west-1".

Example:
  Default: "us-east-1"
EOF
  type    = string
  default = "us-east-1"
}
