# Set required provider
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.63.1"
    }
  }
}

# Configure project
provider "google" {
  project = var.project_id
}
