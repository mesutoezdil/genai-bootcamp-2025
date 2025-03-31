# OPEA ChatQnA AWS Deployment Guide

This guide details how to deploy the **ChatQnA** application from the [OPEA GenAI Examples repository](https://github.com/opea-project/GenAIExamples/tree/main/ChatQnA) onto Amazon Web Services (AWS) using **Terraform**. The goal is to automate both infrastructure creation and application setup using Infrastructure-as-Code (IaC) principles, while also providing guidance on secure practices and reliable troubleshooting methods.

---

## Table of Contents

1. [Introduction](#1-introduction)  
2. [Prerequisites](#2-prerequisites)  
3. [Project Structure](#3-project-structure)  
4. [AWS Provider & SSH Key Setup](#4-aws-provider--ssh-key-setup)  
5. [Terraform Workflow](#5-terraform-workflow)  
6. [Security Best Practices](#6-security-best-practices)  
7. [Configuring Variables](#7-configuring-variables)  
8. [Deployment Steps](#8-deployment-steps)  
9. [Troubleshooting & Logs](#9-troubleshooting--logs)  
10. [Accessing ChatQnA](#10-accessing-chatqna)  
11. [Performance & Scaling](#11-performance--scaling)  
12. [Cleanup & Cost Management](#12-cleanup--cost-management)  
13. [Conclusion](#13-conclusion)

---

## 1. Introduction

**ChatQnA** is a cutting-edge conversational AI solution developed under the **OPEA** umbrella, leveraging advanced **GenAI** components for real-time question and answer experiences. By integrating **Retrieval-Augmented Generation (RAG)** and other modern NLP techniques, ChatQnA can deliver robust, context-aware responses in diverse use cases.

This guide describes how to deploy ChatQnA on **AWS** using Terraform—covering the entire process from setting up your environment to verifying a successful deployment. The same concepts can be adapted to other platforms such as **Google Cloud Platform (GCP)**, **IBM Cloud**, **Microsoft Azure**, or **Oracle Cloud Infrastructure**. For platform-specific instructions, consult the [Official ChatQnA Documentation](https://opea-project.github.io/latest/getting-started/README.html).

---

## 2. Prerequisites

Before proceeding, ensure you have:

1. **Terraform (v5.0.0 or newer)**  
   - [Terraform Downloads](https://www.terraform.io/downloads.html)
   - Verify by running `terraform --version`.

2. **AWS CLI**  
   - [AWS CLI Installation Guide](https://aws.amazon.com/cli/)
   - Confirm you can run `aws configure` and have valid credentials.

3. **AWS Account**  
   - Must have permissions to create and manage EC2, VPC, Security Groups, IAM roles, and any required networking resources.

4. **SSH Key Pair**  
   - A valid SSH key pair on your local machine. Make sure the private key is secured with correct permissions (`chmod 600 <keyfile>`).

5. **Hugging Face API Token**  
   - Obtain the token from [Hugging Face settings](https://huggingface.co/settings/tokens). This is required for model access or fine-tuning tasks that leverage Hugging Face endpoints.

6. **Git** (Optional)  
   - If you plan to clone or manage the deployment scripts from a Git repository.

> **Note**: Familiarity with **Terraform** and basic AWS concepts (e.g., VPC, subnets, security groups) is highly recommended to follow best practices and debug any issues.

---

## 3. Project Structure

A recommended structure is outlined below to maintain clarity between Terraform configuration files, variables, and modules:

```plaintext
opea-chatqna-deployment/
├── main.tf                     # Primary Terraform configuration
├── variables.tf                # Definitions of input variables
├── outputs.tf                  # Definitions of output values
├── terraform.tfvars            # File containing variable values (local & not committed)
├── terraform.tfvars.example    # Sample variable file demonstrating expected inputs
├── modules/                    # Directory for reusable Terraform modules
│   ├── network/                # Module for VPC, subnets, IGW, NAT, etc.
│   └── ec2/                    # Module for provisioning EC2 instances
│       ├── linux-ssh-config.tpl  # Template to generate SSH config
└── README.md                   # This guide or a variant of it
```

- **`main.tf`**: References modules and defines the overarching AWS infrastructure (e.g., VPC creation, EC2 instance launches).  
- **`variables.tf`**: Specifies variables like AWS region, instance type, SSH key paths, etc.  
- **`terraform.tfvars`**: Actual values used during deployment. This file should *not* be committed to version control if it contains sensitive data.  
- **`terraform.tfvars.example`**: Demonstrates the expected structure of `terraform.tfvars`.  
- **`modules/`**: Contains specialized Terraform modules for networking, compute, or any further infrastructure sub-component.  

---

## 4. AWS Provider & SSH Key Setup

### AWS Provider Configuration

In `main.tf` or a dedicated provider configuration file, you should specify:

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
  profile = "sunbirdai"  # or your chosen AWS CLI profile name
}
```

Ensure your AWS CLI is **configured with the specified profile** (`sunbirdai`, in this example). You can verify this via:

```bash
aws configure --profile sunbirdai
```

### SSH Key Management

The provisioning process will:

1. **Import** your local SSH public key into AWS as an EC2 key pair.  
2. **Generate** an SSH config snippet referencing your new key pair and EC2 instance details (using `linux-ssh-config.tpl` or a similar template).  
3. **Enable** you to easily SSH into your newly created EC2 instance(s) using the private key on your local machine.

> **Important**: Always confirm that your local SSH key paths match those in your Terraform variables. Also ensure your private key is **secure** and not stored in a publicly accessible location.

---

## 5. Terraform Workflow

Below are the standard Terraform commands you will use throughout the deployment and lifecycle management process.

1. **Initialize the Workspace**  
   Initializes providers, modules, and backend configuration:
   ```bash
   terraform init
   ```

2. **Validate Configuration**  
   Checks for syntax correctness and catches common misconfigurations:
   ```bash
   terraform validate
   ```

3. **Format Configuration Files**  
   Auto-formats all `.tf` files to Terraform’s style conventions:
   ```bash
   terraform fmt -recursive
   ```

4. **Generate Execution Plan**  
   Previews the changes to be applied, showing a summary of what Terraform will do:
   ```bash
   terraform plan
   ```

5. **Apply the Changes**  
   Provisions resources and configures them on AWS:
   ```bash
   terraform apply --auto-approve
   ```
   > Using `--auto-approve` bypasses interactive confirmation. Consider removing it in production to enforce a manual check step.

6. **Destroy Infrastructure**  
   Removes all the managed resources. Exercise caution:
   ```bash
   terraform destroy --auto-approve
   ```

---

## 6. Security Best Practices

Securely managing both infrastructure and application data on AWS is paramount. Here are additional recommendations:

1. **Store Sensitive Values Properly**  
   - Keep secrets (e.g., Hugging Face API tokens) in `terraform.tfvars` or use environment variables.  
   - Add `terraform.tfvars` to `.gitignore` so it never appears in version control.

2. **Use Encrypted Remote State**  
   - Instead of storing `terraform.tfstate` locally, configure remote storage on **AWS S3** with server-side encryption (SSE-KMS) and tight IAM permissions.

3. **Lock Terraform State**  
   - Use **DynamoDB** table locking to prevent concurrency conflicts during deployments.

4. **Restrict SSH Ingress**  
   - Limit SSH access to your own IP range or authorized corporate VPN networks.  
   - Regularly rotate SSH keys for better security posture.

5. **Update & Patch**  
   - Keep your base AMIs and Docker images updated with security patches.  
   - Use EC2 Image Builder or other CI/CD methods for regular OS patching.

6. **AWS Secrets Manager**  
   - Consider using **AWS Secrets Manager** or **Parameter Store** to manage tokens, credentials, and other sensitive data. This is particularly useful for production or multi-team environments.

7. **Least Privilege IAM**  
   - Set IAM roles and policies granting only the required permissions to Terraform and any created EC2 instances. Avoid using overly broad admin roles.

---

## 7. Configuring Variables

### Creating Your `terraform.tfvars` File

Start by duplicating the sample file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Open `terraform.tfvars` and insert your deployment-specific values:

```hcl
aws_region           = "us-east-1"
instance_type        = "m7i.4xlarge"
ssh_public_key_path  = "~/.ssh/id_rsa.pub"
ssh_private_key_path = "~/.ssh/id_rsa"
huggingface_token    = "your-huggingface-token"
```

> **Tip**: Use a more modest instance type (e.g., `t3.large`) in lower environments or for quick tests, then scale up for production usage.

### Example Variables Explanation

1. **`aws_region`**: The AWS region where your resources will reside.  
2. **`instance_type`**: The EC2 instance type for the ChatQnA server (influences performance & cost).  
3. **`ssh_public_key_path`** & **`ssh_private_key_path`**: Paths to your local SSH keys for secure connections.  
4. **`huggingface_token`**: Grants ChatQnA access to models or endpoints on Hugging Face.

---

## 8. Deployment Steps

Below is a typical end-to-end procedure for provisioning ChatQnA on AWS:

1. **Navigate to Deployment Directory**  
   ```bash
   cd opea-chatqna-deployment
   ```

2. **Initialize Terraform**  
   ```bash
   terraform init
   ```

3. **Validate & Format**  
   ```bash
   terraform validate
   terraform fmt -recursive
   ```

4. **Plan Infrastructure**  
   ```bash
   terraform plan
   ```
   Review the plan output to ensure the resources and configurations match your expectations.

5. **Apply & Deploy**  
   ```bash
   terraform apply --auto-approve
   ```
   Terraform will create the necessary AWS resources: VPC, subnets, security groups, and EC2 instances with Docker installed and ChatQnA configured.

6. **Obtain SSH Config**  
   Upon successful completion, a file named something like `ssh_config_opea-chatqna.txt` is generated. Run:
   ```bash
   cat ./ssh_config_opea-chatqna.txt | bash
   ```
   This loads SSH configuration details into your local environment, creating or appending to a `.ssh/config` block.

7. **Connect & Verify**  
   - **SSH** to your instance:  
     ```bash
     ssh ubuntu@<instance-ip>
     ```
   - **Logs**: Examine `cloud-init-output.log` or Docker logs to confirm successful startup.

> **Note**: If the instance fails to initialize properly, check your AWS region or instance type for availability and cost constraints.

---

## 9. Troubleshooting & Logs

Even a well-tested deployment can encounter hiccups. Below are common issues and their resolutions:

1. **SSH Connection Denied**  
   - Ensure `ssh_public_key_path` matches the exact name of your public key file.  
   - Double-check the security group inbound rules for port `22`.  
   - Confirm your local IP has not changed if you are restricting inbound SSH by IP.

2. **Cloud-Init & Docker Failures**  
   - Log in via SSH and inspect:
     ```bash
     sudo cat /var/log/cloud-init-output.log
     ```
   - **Docker Logs**:
     ```bash
     docker ps -a
     docker logs vllm-service
     docker logs chatqna-frontend
     ```
   - Look for error messages indicating configuration or environment variable problems.

3. **Hugging Face Token Issues**  
   - Validate the token on Hugging Face to ensure it is active and has the required scopes.  
   - Confirm the `huggingface_token` is spelled correctly in `terraform.tfvars`.

4. **API / Web Page Not Accessible**  
   - Verify that port `80` (or whichever port is used) is open in the associated security group.  
   - Confirm the EC2 instance has a public IP assigned and that you’re using the correct IP or DNS name.

5. **Terraform State Lock Errors**  
   - If you use remote state, ensure the DynamoDB table for state locking is accessible and you have correct IAM permissions.

---

## 10. Accessing ChatQnA

Once infrastructure and application services are running:

1. **Get the Public IP**  
   - Terraform typically outputs the public IP address or DNS for the EC2 instance.  
   - Alternatively, find it in the **EC2** console.

2. **Navigate via Browser**  
   - Go to:
     ```
     http://<instance-public-ip>:80
     ```
   - You should see the ChatQnA UI. If you use an alternate port or domain, adjust accordingly.

3. **Interactive Queries**  
   - Type your query in the ChatQnA interface (e.g., “What is OPEA?”).  
   - For more context-rich answers, upload relevant documents so the system can use them for RAG-based responses.

4. **Further Customizations**  
   - You can configure environment variables to enable advanced features, like caching or custom model endpoints.  
   - See the official [ChatQnA documentation](https://opea-project.github.io/latest/getting-started/README.html) for instructions on advanced features.

---

## 11. Performance & Scaling

To handle higher loads or reduce latency:

1. **EC2 Auto Scaling**  
   - Implement an Auto Scaling Group (ASG) for horizontally scaling ChatQnA instances.  
   - Use a Load Balancer (ALB or NLB) to distribute traffic.

2. **Vertical Scaling**  
   - Switch to a more powerful instance type (e.g., `m7i.8xlarge`) for complex tasks or heavier concurrency.

3. **Caching & CDN**  
   - For static assets, configure an AWS S3 bucket + CloudFront distribution.  
   - Use an in-memory cache (Redis/ElastiCache) for frequently accessed data.

4. **External Datastore**  
   - If ChatQnA logs data or needs persistent storage, integrate with Amazon RDS or DynamoDB, depending on your requirements.

---

## 12. Cleanup & Cost Management

AWS costs can accumulate quickly. To avoid unexpected bills:

1. **Destroy the Infrastructure**  
   ```bash
   terraform destroy --auto-approve
   ```
   Removes all resources created by Terraform.

2. **Check for Orphaned Resources**  
   - Log in to the AWS Console and verify that no leftover resources (e.g., EBS volumes or Elastic IPs) remain.

3. **Use Budget Alarms**  
   - Configure AWS Budgets to receive notifications if your monthly costs exceed a threshold.

4. **Use Spot Instances**  
   - For non-critical or ephemeral usage, consider Spot Instances to reduce compute costs.

---

## 13. Conclusion

Congratulations! You have successfully deployed the **OPEA ChatQnA** application on AWS using Terraform. This guide provided:

- Detailed **infrastructure** setup steps.  
- **Security best practices** for protecting your cloud environment.  
- **Troubleshooting** pointers for common deployment issues.  
- **Performance and scaling** recommendations for heavier workloads or production scenarios.  
- **Cost management** insights to keep expenses in check.

For additional information, including advanced configurations, feature toggles, or specialized integration with other OPEA services, consult the [Official ChatQnA Documentation](https://opea-project.github.io/latest/getting-started/README.html). If you run into any challenges or have questions, feel free to open an issue on the [OPEA GitHub repository](https://github.com/opea-project/GenAIExamples) or reach out to the OPEA community for support.
