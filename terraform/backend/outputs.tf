output "state_bucket_name" {
  value       = module.gcs_terraform_state_bucket.gcs_bucket_name
  description = "Name of the GCS backend bucket."
}

output "sa_email" {
  value       = module.sa.email
  description = "Email of the GH Actions deployer SA."
}

output "workload_id_provider_name" {
  value       = module.wif.provider_name
  description = "Name of the ID pool provider for GitHub."
}