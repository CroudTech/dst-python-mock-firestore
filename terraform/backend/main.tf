# Backend bucket, this will be used for the state
module "gcs_terraform_state_bucket" {
  source      = "git::ssh://git@github.com/CroudTech/dst-terraform-module-gcs-backend?ref=tags/v1.1.1"
  environment = var.environment
  project_id  = var.project_id
  region      = var.region
}

# Service Account to deploy to GH Actions
module "sa" {
  source = "git::ssh://git@github.com/CroudTech/dst-terraform-module-service-accounts//dst-terraform-submodule-gh-actions-deployer?ref=tags/v2.0.0"
  # Region, env, project basics
  project_id  = var.project_id
  environment = var.environment
  region      = var.region
  # Key creation, disabled in this case
  create_json_key = false
  export_json_key = false
  # Only grant access to necessary resources (right now editor should be fine)
  # Add all the roles you might need for running Terraform against GCP
  extra_roles            = ["roles/editor"]
  has_editor_permissions = false
}

# Workload Identity Federation for GitHub Actions
module "wif" {
  source = "git::ssh://git@github.com/CroudTech/dst-terraform-module-workload-identity-federation?ref=tags/v1.0.1"

  # Location
  project_id  = var.project_id
  environment = var.environment
  region      = var.region

  # Repo config
  repo = var.repo
  org  = "CroudTech"

  # Provider
  provider_name = "github"
  provider_uri  = "https://token.actions.githubusercontent.com"
  mappings = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
  }

  # SA config
  service_accounts = [module.sa.name]
}
