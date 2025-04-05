locals {
  tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "terraform"
    CreatedAt   = timestamp()
  }
}
