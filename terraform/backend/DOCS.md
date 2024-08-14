<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_google"></a> [google](#requirement\_google) | 4.63.1 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_gcs_terraform_state_bucket"></a> [gcs\_terraform\_state\_bucket](#module\_gcs\_terraform\_state\_bucket) | git::ssh://git@github.com/CroudTech/dst-terraform-module-gcs-backend | tags/v1.1.1 |
| <a name="module_sa"></a> [sa](#module\_sa) | git::ssh://git@github.com/CroudTech/dst-terraform-module-service-accounts//dst-terraform-submodule-gh-actions-deployer | tags/v2.0.0 |
| <a name="module_wif"></a> [wif](#module\_wif) | git::ssh://git@github.com/CroudTech/dst-terraform-module-workload-identity-federation | tags/v1.0.1 |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_environment"></a> [environment](#input\_environment) | Environment (prod/dev), default dev | `string` | `"dev"` | no |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | n/a | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | GCP region https://cloud.google.com/compute/docs/regions-zones default US | `string` | `"US"` | no |
| <a name="input_repo"></a> [repo](#input\_repo) | Name of the repository in which the WIF is going to be used. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_sa_email"></a> [sa\_email](#output\_sa\_email) | Email of the GH Actions deployer SA. |
| <a name="output_state_bucket_name"></a> [state\_bucket\_name](#output\_state\_bucket\_name) | Name of the GCS backend bucket. |
| <a name="output_workload_id_provider_name"></a> [workload\_id\_provider\_name](#output\_workload\_id\_provider\_name) | Name of the ID pool provider for GitHub. |
<!-- END_TF_DOCS -->