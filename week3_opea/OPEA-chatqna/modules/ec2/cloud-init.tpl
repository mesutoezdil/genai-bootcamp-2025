#cloud-config
package_update: true
package_upgrade: true

packages:
  - apt-transport-https
  - ca-certificates
  - curl
  - gnupg
  - lsb-release
  - git
  - wget

write_files:
  # Script to download and install Docker
  - path: /home/ubuntu/install_docker.sh
    owner: ubuntu:ubuntu
    permissions: "0755"
    content: |
      #!/bin/bash
      cd /home/ubuntu
      wget https://raw.githubusercontent.com/opea-project/GenAIExamples/refs/heads/main/ChatQnA/docker_compose/install_docker.sh
      chmod +x install_docker.sh
      ./install_docker.sh

      # Add the ubuntu user to the Docker group
      sudo usermod -aG docker ubuntu

  - path: /home/ubuntu/start_chatqna.sh
    owner: ubuntu:ubuntu
    permissions: "0755"
    content: |
      #!/bin/bash

      export RELEASE_VERSION=${opea_release_version}
      export host_ip="localhost"
      export HUGGINGFACEHUB_API_TOKEN="${huggingface_token}"

      # Clone the repository and checkout the specified release
      git clone https://github.com/opea-project/GenAIExamples.git
      cd GenAIExamples
      git checkout tags/v$${RELEASE_VERSION}

      # Navigate to the appropriate directory
      cd ChatQnA/docker_compose/intel/cpu/xeon/

      # Load environment variables
      source set_env.sh

      # Start the services
      docker compose -f compose.yaml up -d

      # Wait for the services to be ready
      echo "Waiting for services to start..."
      while ! docker logs vllm-service 2>&1 | grep -q "Application startup complete."; do
        sleep 10
        echo "vllm-service is still starting..."
      done

      echo "ChatQnA deployment is complete! Access the application at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):80"

runcmd:
  - chmod +x /home/ubuntu/install_docker.sh
  - chmod +x /home/ubuntu/start_chatqna.sh
  - su - ubuntu -c "/home/ubuntu/install_docker.sh"
  - su - ubuntu -c "/home/ubuntu/start_chatqna.sh"
  - echo "ChatQnA deployment started at: $(date)" > /home/ubuntu/deployment_status.txt

final_message: "The system is fully operational after $UPTIME seconds"
