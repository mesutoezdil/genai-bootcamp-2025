#########################################################################
# Terraform Configuration: AWS Network Infrastructure Setup
#
# This configuration file defines the following AWS resources for the
# project:
#   1. A Virtual Private Cloud (VPC) for isolated networking.
#   2. An Internet Gateway (IGW) to enable external connectivity.
#   3. A public subnet that automatically assigns public IP addresses.
#   4. A Route Table that directs outbound traffic through the IGW.
#   5. A Route Table Association linking the public subnet with the Route Table.
#   6. A Security Group controlling inbound and outbound traffic.
#
# Variables such as the VPC CIDR block, AWS region, and project name are
# defined externally to ensure reusability and flexibility.
#########################################################################

# Create a Virtual Private Cloud (VPC)
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr_block  # Define the IP range for the VPC.
  enable_dns_hostnames = true                # Enable DNS hostnames for instances.
  enable_dns_support   = true                # Enable DNS resolution within the VPC.

  # Tagging the VPC for easier identification and management.
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Create an Internet Gateway (IGW) for the VPC to allow outbound internet access.
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id  # Associate the IGW with the VPC.

  # Tag the IGW for clarity in the AWS console.
  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Create a public subnet within the VPC.
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id

  # Calculate a subnet CIDR block based on the VPC CIDR block. This splits the VPC into smaller networks.
  cidr_block              = cidrsubnet(var.vpc_cidr_block, 8, 1)

  # Automatically assign a public IP address to instances launched in this subnet.
  map_public_ip_on_launch = true

  # Specify the availability zone. Adjust the zone suffix as needed.
  availability_zone       = "${var.aws_region}a"

  # Tag the subnet for easy identification.
  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

# Create a Route Table for directing traffic from the public subnet.
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  # Define a default route that directs all outbound traffic (0.0.0.0/0) to the Internet Gateway.
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  # Tag the Route Table with a descriptive name.
  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

# Associate the public subnet with the created Route Table to enable internet access.
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id         # Reference the public subnet.
  route_table_id = aws_route_table.public.id     # Reference the public route table.
}

# Create a Security Group to manage inbound and outbound traffic for instances.
resource "aws_security_group" "main" {
  name        = "${var.project_name}-sg"  # Name of the security group.
  description = "Security group for OPEA ChatQnA application resources"
  vpc_id      = aws_vpc.main.id           # Associate the security group with the VPC.

  # Allow inbound SSH connections (port 22) from any source for administrative access.
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow SSH access from any IP address"
  }

  # Allow inbound HTTP traffic (port 80) from any source for web application access.
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP access for web traffic"
  }

  # Define an egress rule to allow all outbound traffic to any destination.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # "-1" signifies all protocols.
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  # Tag the security group for clear identification in the AWS console.
  tags = {
    Name = "${var.project_name}-sg"
  }
}
