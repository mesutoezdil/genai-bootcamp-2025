# OPEA ChatQnA Deployment: An Advanced Step-by-Step Guide

Welcome to the definitive guide for deploying the ChatQnA application from the OPEA GenAI Examples repository. This guide is crafted to support multiple cloud platforms—including AWS, GCP, IBM Cloud, Microsoft Azure, and Oracle Cloud Infrastructure—empowering you to choose the environment that best meets your project needs.

---

## 1. Introduction

OPEA combines cutting-edge microservice components and practical examples to deliver a powerful, scalable GenAI platform. This guide details the steps to deploy ChatQnA, enabling you to harness the potential of large language models (LLM) and retrieval-augmented generation (RAG) for advanced question-answering applications.

---

## 2. Core Components Overview

Before you dive in, it’s essential to understand the two pillars of the OPEA ecosystem:

- **GenAIComps**:  
  A robust suite of microservices offering functionalities such as LLM inference, embeddings, and reranking. These components form the backbone of your service architecture.

- **GenAIExamples**:  
  A collection of ready-to-deploy solutions that showcase the practical use of GenAIComps. The ChatQnA solution is one such example that demonstrates how to integrate and deploy these microservices for conversational AI tasks.

---

## 3. System Prerequisites

Ensure you have the following in place before starting the deployment:

- **Cloud Account**: An active account on your target cloud platform (AWS, GCP, etc.).
- **SSH Access**: A valid SSH key pair for secure instance connectivity.
- **Docker**: Ability to install or run Docker.
- **Git**: Installed and configured for source code management.
- **Basic Networking Knowledge**: Familiarity with VPC, subnets, and security groups.

---

## 4. AWS Deployment Walkthrough

### 4.1 Provisioning the Virtual Server

#### **Step 1: Launch an EC2 Instance**

1. **Access the AWS Management Console**  
   Visit the [AWS Console](https://console.aws.amazon.com/console/home) and navigate to **EC2**.

2. **Start Instance Launch**  
   Click **Launch instance** and follow the wizard.

3. **Configure Instance Details**  
   - **Naming**: Enter a descriptive name (e.g., `OPEA-ChatQnA-Server`).
   - **AMI Selection**: Choose Ubuntu (`ami-04dd23e62ed049936`).
   - **Instance Type**: For Intel-based workloads, select a powerful instance such as `m7i.4xlarge` or above.  
     > _Tip_: For guidance on optimal configurations, check the [AWS and Intel reference](https://aws.amazon.com/intel/).

4. **Configure Security and SSH**  
   - **Key Pair**: Create or select an SSH key pair.
   - **Security Groups**: Either choose an existing group or create a new one with:
     - **SSH (port 22)** enabled.
     - **HTTP (port 80)** enabled.

5. **Storage Configuration**  
   Set the storage size to **100 GiB**.

6. **Launch the Instance**  
   Confirm your settings and click **Launch instance**. A success notification will appear once the instance is running.

#### **Step 2: Configure Security Settings**

1. **Connect to Your Instance**  
   Follow the **Connect** instructions from the AWS Console to access your instance via SSH.

2. **Modify Inbound Rules**  
   - Navigate to the associated **Security Group**.
   - Edit inbound rules to add a custom rule for HTTP:
     - **Type**: Custom TCP
     - **Port Range**: 80
     - **Source**: 0.0.0.0/0  
   > _Reference_: [AWS Security Groups Documentation](https://docs.aws.amazon.com/finspace/latest/userguide/step5-config-inbound-rule.html).

3. **Apply and Save**  
   Confirm the changes by clicking **Save rules**.

---

## 5. Deploying the ChatQnA Application

### 5.1 Docker Installation

Run the following commands on your virtual server to install Docker:

```bash
wget https://raw.githubusercontent.com/opea-project/GenAIExamples/refs/heads/main/ChatQnA/docker_compose/install_docker.sh
chmod +x install_docker.sh
./install_docker.sh
```

After installation, configure Docker to run without root privileges by following the [post-install instructions](https://docs.docker.com/engine/install/linux-postinstall/).

### 5.2 Repository Setup and Release Checkout

1. **Set the Release Version**  
   Define your desired release version as an environment variable:
   ```bash
   export RELEASE_VERSION=<your-release-version>
   ```

2. **Clone the Repository**  
   ```bash
   git clone https://github.com/opea-project/GenAIExamples.git
   cd GenAIExamples
   ```

3. **Checkout the Specific Release**  
   ```bash
   git checkout tags/v${RELEASE_VERSION}
   ```

### 5.3 Environment Configuration

Configure essential environment variables required by the application:

```bash
export host_ip="localhost"
export HUGGINGFACEHUB_API_TOKEN="Your_Huggingface_API_Token"
```

For environments behind a firewall, set your proxy settings:

```bash
export no_proxy=${your_no_proxy},$host_ip
export http_proxy=${your_http_proxy}
export https_proxy=${your_http_proxy}
```

Additionally, customize any specific settings in the `set_env.sh` file before sourcing it:

```bash
cd ChatQnA/docker_compose/intel/cpu/xeon/
source set_env.sh
```

### 5.4 Launching the Services

With Docker installed and environment variables set, launch the ChatQnA services using Docker Compose:

```bash
docker compose -f compose.yaml up -d
```

> **Note**: Service initialization may take several minutes. Monitor logs to confirm that all components are up and running.

#### **Verifying Startup**

Check the logs for the `vllm-service` to ensure proper startup:

```bash
docker logs vllm-service | grep Complete
```

A successful startup is indicated by messages like:

```plaintext
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

Also, run `docker ps -a` to verify that all services are active and that the Docker image versions correspond to your defined `RELEASE_VERSION`.

---

## 6. Interacting with ChatQnA

### 6.1 Accessing the User Interface

Open your web browser and enter the following URL (replace `{public_ip}` with your instance’s public IP):

```
http://{public_ip}:80
```

For users utilizing port forwarding or load balancers, you may need to use `http://localhost:80` or the designated virtual IP.

### 6.2 Testing the ChatQnA Functionality

Once the interface loads, try posing a query such as “What is OPEA?” to see the system’s response. Initially, the model may provide a generic or unexpected answer due to gaps in its training data regarding OPEA.

### 6.3 Enhancing Accuracy with RAG

To refine responses, leverage Retrieval-Augmented Generation (RAG) by uploading a contextual PDF:

- **Download the Context Document**:  
  Obtain the [OPEA Document](https://opea-project.github.io/latest/_downloads/41c91aec1d47f20ca22350daa8c2cadc/what_is_opea.pdf).

- **Upload Through the UI**:  
  Use the interface to upload the document, allowing the model to reference up-to-date and contextual information.

Compare the results before and after uploading the document:

- **Without Context**:  
  The model’s response may be generic.

- **With RAG-Enhanced Context**:  
  The responses become more precise and context-aware.

Example screenshots:

![Chat Interface](https://opea-project.github.io/latest/_images/chat_ui_response.png)

![Chat Interface with RAG](https://opea-project.github.io/latest/_images/chat_ui_response_rag.png)

---

## 7. Final Thoughts

This guide has walked you through setting up a robust environment on AWS for deploying the ChatQnA application from OPEA GenAI Examples. By following these steps, you will be able to harness the power of advanced conversational AI and customize your deployment to fit your unique operational needs.

For further details, troubleshooting, or advanced configurations, refer to the complete [ChatQnA Guide](/tutorial/ChatQnA/ChatQnA_Guide.rst).

Happy deploying and exploring the capabilities of OPEA!