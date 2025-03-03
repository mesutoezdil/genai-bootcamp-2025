resource "aws_key_pair" "project_key" {
  key_name   = "${var.project_name}-key"
  public_key = file(var.ssh_public_key_path)
}

resource "aws_instance" "project_instance" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.security_group_id]
  key_name               = aws_key_pair.project_key.key_name

  root_block_device {
    volume_size = var.root_volume_size
    volume_type = "gp3"
  }

  user_data = templatefile("${path.module}/userdata.tftpl", {
    huggingface_token    = var.huggingface_token
    opea_release_version = var.opea_release_version
  })

  tags = {
    Name = "${var.project_name}-instance"
  }

  provisioner "local-exec" {
    command = templatefile("${path.module}/${var.host_os}-ssh-config.tpl", {
      hostname     = self.public_ip,
      user         = "ubuntu",
      identityfile = "~/.ssh/id_open_project"
    })
    interpreter = var.host_os == "windows" ? ["Powershell", "-Command"] : ["bash", "-c"]
  }
}

# Generate a local file with the rendered SSH configuration (for Linux)
resource "local_file" "linux_ssh_config" {
  content = templatefile("${path.module}/linux-ssh-config.tpl", {
    hostname     = aws_instance.project_instance.public_ip
    user         = "ubuntu"
    identityfile = var.ssh_private_key_path
  })
  filename = "${path.cwd}/ssh_config_${var.project_name}.txt"
}

# Render the cloud-init template with the token redacted for security
resource "local_file" "rendered_cloud_init" {
  content = templatefile("${path.module}/cloud-init.tpl", {
    huggingface_token    = "REDACTED"
    opea_release_version = var.opea_release_version
  })
  filename = "${path.module}/rendered-cloud-init.yaml"
}
