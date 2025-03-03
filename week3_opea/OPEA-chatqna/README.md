Below is a reimagined, extended, and refined version of the deployment guide. This version is restructured with enhanced clarity, additional context, and extended troubleshooting and security details to ensure a smooth deployment of the OPEA ChatQnA application on AWS.

---

# OPEA ChatQnA AWS Deployment Guide

This guide details how to deploy the ChatQnA application from the [OPEA GenAI Examples repository](https://github.com/opea-project/GenAIExamples/tree/main/ChatQnA) using Terraform. It follows the official OPEA documentation and leverages infrastructure-as-code (IaC) to automate the provisioning of both AWS infrastructure and application deployment.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Provider & SSH Key Setup](#provider--ssh-key-setup)
5. [Terraform Workflow Commands](#terraform-workflow-commands)
6. [Security Best Practices](#security-best-practices)
7. [Variable Configuration](#variable-configuration)
8. [Deployment Steps](#deployment-steps)
9. [Troubleshooting & Logs](#troubleshooting--logs)
10. [Accessing ChatQnA](#accessing-chatqna)
11. [Conclusion](#conclusion)

---

## 1. Introduction

OPEA’s ChatQnA application is a state-of-the-art conversational AI solution designed to provide interactive question-and-answer capabilities using advanced GenAI components. This guide explains how to deploy ChatQnA on AWS, but similar concepts can be applied across cloud platforms such as GCP, IBM Cloud, Azure, and Oracle Cloud Infrastructure. For further deployment targets, please consult the [official ChatQnA documentation](https://opea-project.github.io/latest/getting-started/README.html).

---

## 2. Prerequisites

Before you begin, ensure you have the following:

- **Terraform**: Version 5.0.0 or newer ([download here](https://www.terraform.io/downloads.html)).
- **AWS CLI**: Installed and configured with appropriate credentials ([AWS CLI Installation](https://aws.amazon.com/cli/)).
- **AWS Account**: With sufficient permissions to create EC2, VPC, Security Groups, and other resources.
- **SSH Key Pair**: A valid SSH key pair on your local machine.
- **Hugging Face API Token**: Obtain your token from [Hugging Face](https://huggingface.co/settings/tokens) for model access.

---

## 3. Project Structure

The repository is organized to clearly separate main configuration, variable definitions, outputs, and reusable modules. Below is the recommended directory structure:

```plaintext
opea-chatqna-deployment/
├── main.tf                     # Primary Terraform configuration
├── variables.tf                # Input variables definitions
├── outputs.tf                  # Outputs definitions for post-deployment
├── terraform.tfvars            # Local variable values (not committed)
├── terraform.tfvars.example    # Example variable file for guidance
├── modules/                    # Reusable Terraform modules
│   ├── network/                # Module for networking (VPC, subnets, IGW, etc.)
│   └── ec2/                    # Module for provisioning EC2 instances
│       ├── linux-ssh-config.tpl # Template for generating SSH config
└── README.md                   # This deployment guide
```

---

## 4. Provider & SSH Key Setup

### AWS Provider Configuration

The deployment uses the latest AWS provider (version ~> 5.89.0). Ensure you have the correct AWS CLI profile configured, as this project uses a specific profile (e.g., "sunbirdai").

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "sunbirdai"
}
```

### SSH Key Management

The deployment process will:

1. Create an AWS key pair using your local SSH public key.
2. Generate an SSH configuration snippet to streamline connecting to your EC2 instance.
3. Utilize your SSH private key for secure remote access.

For instructions on creating and configuring SSH key pairs, see [this guide](./ssh.md).

---

## 5. Terraform Workflow Commands

Before deploying your infrastructure, follow these Terraform commands:

- **Initialize Workspace**:  
  ```bash
  terraform init
  ```

- **Validate Configuration**:  
  ```bash
  terraform validate
  ```

- **Format Configuration Files**:  
  ```bash
  terraform fmt -recursive
  ```

- **Generate Execution Plan**:  
  ```bash
  terraform plan
  ```

- **Apply the Changes**:  
  ```bash
  terraform apply --auto-approve
  ```

- **Destroy Infrastructure**:  
  ```bash
  terraform destroy --auto-approve
  ```

---

## 6. Security Best Practices

Security is paramount when deploying cloud infrastructure. Consider the following recommendations:

- **Sensitive Information**:  
  Store sensitive variables (e.g., API tokens, private keys) in `terraform.tfvars` and ensure this file is listed in `.gitignore`.

- **Remote State Management**:  
  Use encrypted remote state storage (e.g., AWS S3 with server-side encryption) to protect sensitive data.

- **AWS Secrets Management**:  
  Consider using AWS Secrets Manager or Parameter Store for managing secrets in production environments.

- **SSH Key Permissions**:  
  Ensure that your SSH private key has strict permissions (e.g., `chmod 600`).

- **Security Group Rules**:  
  Restrict inbound rules to only allow traffic from trusted IP ranges.

---

## 7. Variable Configuration

Set your configuration values by copying the example variable file and editing it with your specific details:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with values similar to:

```hcl
aws_region           = "us-east-1"              # AWS region to deploy resources
instance_type        = "m7i.4xlarge"            # Instance type for ChatQnA (recommended for performance)
ssh_public_key_path  = "~/.ssh/id_rsa.pub"      # Path to your public SSH key
ssh_private_key_path = "~/.ssh/id_rsa"          # Path to your private SSH key
huggingface_token    = "your-huggingface-token" # API token from Hugging Face
```

**Important:** Never commit your `terraform.tfvars` file to version control as it may contain sensitive data.

---

## 8. Deployment Steps

Follow these steps to deploy the ChatQnA application on AWS:

### Step 1: Set Up Your Local Environment

- Navigate to the deployment directory:
  ```bash
  cd opea-chatqna-deployment
  ```

- Create your `terraform.tfvars` file with your environment-specific values.

### Step 2: Initialize and Validate Terraform

- Initialize the Terraform working directory:
  ```bash
  terraform init
  ```

- Validate your configuration files:
  ```bash
  terraform validate
  ```

### Step 3: Plan and Apply Infrastructure

- Generate an execution plan:
  ```bash
  terraform plan
  ```

- Deploy the infrastructure:
  ```bash
  terraform apply --auto-approve
  ```

### Step 4: Configure SSH Access

After deployment, an SSH configuration file is generated. To load this configuration, run:

```bash
cat ./ssh_config_opea-chatqna.txt | bash
```

This step simplifies the process of connecting to your EC2 instance.

### Step 5: Verify and Access the Application

- **EC2 Instance**:  
  Use the outputs to retrieve the public IP of your instance.

- **ChatQnA Application**:  
  Open your browser and navigate to:
  ```
  http://{public_ip}:80
  ```
  Replace `{public_ip}` with the actual IP from the Terraform outputs.

### Step 6: Post-Deployment Verification

- **Cloud-Init Logs**:  
  To check initialization logs:
  ```bash
  ssh ubuntu@<instance-ip> 'sudo cat /var/log/cloud-init-output.log'
  ```

- **Docker Service Logs**:  
  Verify that key services are running:
  ```bash
  ssh ubuntu@<instance-ip>
  docker logs vllm-service | grep Complete
  ```

- **Service Status**:  
  Confirm that all Docker containers are active:
  ```bash
  docker ps -a
  ```

---

## 9. Troubleshooting & Logs

If you encounter issues, consider the following troubleshooting tips:

- **SSH Connectivity Issues**:
  - Verify that the paths to your SSH keys in `terraform.tfvars` are correct.
  - Check that your security group rules permit SSH (port 22) from your IP.
  - Ensure your private key has the correct file permissions (`chmod 600`).

- **Application Startup Issues**:
  - Review cloud-init logs for errors:
    ```bash
    ssh ubuntu@<instance-ip> 'sudo cat /var/log/cloud-init-output.log'
    ```
  - Check Docker container logs for any service-specific errors:
    ```bash
    docker logs vllm-service
    ```

- **Hugging Face Token Issues**:
  - Ensure your Hugging Face API token is valid and has necessary permissions.
  - Re-check the environment variable configuration for any typos.

---

## 10. Accessing ChatQnA

After a successful deployment, you can interact with the ChatQnA application:

- **Web Interface**:  
  Open your browser and navigate to:
  ```
  http://{public_ip}:80
  ```
  This URL opens the ChatQnA UI where you can enter queries and interact with the model.

- **Sample Interaction**:  
  Try asking: "What is OPEA?"  
  Initially, the model might provide a generic response due to limited context. For improved accuracy, upload a context document (such as the OPEA whitepaper) through the UI to leverage Retrieval-Augmented Generation (RAG).

- **UI Snapshot**:  
  Below is an example of the ChatQnA interface:
  
  ![ChatQnA Interface](./screenshots/chatqna.png)

---

## 11. Conclusion

This comprehensive guide has walked you through the complete process of deploying the OPEA ChatQnA application on AWS using Terraform. By following these detailed steps, you can set up your environment, deploy robust infrastructure, and interact with an advanced conversational AI application. Remember to follow security best practices and consult the troubleshooting section if any issues arise.

For further information and advanced configurations, please refer to the [official ChatQnA documentation](https://opea-project.github.io/latest/getting-started/README.html).

Happy deploying, and enjoy exploring the capabilities of OPEA ChatQnA!