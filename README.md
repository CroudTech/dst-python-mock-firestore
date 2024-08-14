# DST - Repository Template

---
- [How to configure it?](#how-to-configure-it)
- [How to use the Terraform stack?](#how-to-use-the-terraform-stack)
  - [How to structure it?](#how-to-structure-it)
- [Linters](#linters)
- [Pre-Commit Hooks](#pre-commit-hooks)
---

Template for other repositories to scaffold from. It contains the following:
- `.gitignore` --> Very wide `.gitignore` that should cover most of the use cases me have. Feel free to edit it.
- `.github`
  - `CODEOWNERS` --> Example `CODEOWNERS` file for you to fill in.
  - `ISSUE_TEMPLATE/bug_report.md` --> Template for issue bug reports.
  - `pull_request_template.md` --> Template for PRs.
  - `workflows` --> Several workflows already configured.
    - `bump-cleanup.yml` --> Cleanup after a manual version bump.
    - `bump.yml` --> Manual version bump trigger
    - `nightly-release.yml` --> Nightly release cron to facilitate night releases.
    - `pr-lint.yml` --> Linting PR titles.
    - `release.yml` --> Generating automatic releases via Release Please.
  - `extras` --> Extra workflows that might be useful.
    - `terraform-test.yml` --> Testing for Terraform and generating automatic docs (NOTE: THIS WILL EVENTUALLY BE IN THE SHARED ACTIONS REPO).
- `terraform`
  - `backend` --> Terraform code for creating a backend bucket and Workload Identity Federation (WIF) to use a Service Account in GitHub Actions.

## How to configure it?

Some steps to make sure your repo is fully configured:
1. Make sure to edit the `CODEOWNERS` file to add the correct users.
2. Move any workflows to `.github/workflows`.
3. Delete the `CHANGELOG` file to start from scratch.
4. Ensure the linters are correctly configured.

## How to use the Terraform stack?

The Terraform stack that's included is meant to simplify how you implement WIF into your deployments. You should do the following:
1. Create a new `terraform.tfvars` from the example (`cp terraform.tfvars.example terraform.tfvars`).
2. Complete the `terraform.tfvars` with the correct values.
3. Move into the Terraform stack (`cd terraform/backend`).
4. Apply the Terraform stack (`terraform apply`). The Terraform engine will pick up the variables from the `terraform.tfvars`.
5. Verify the changes, and accept them when prompted to.
6. Part of the output of the Terraform command will contain the following:
   1. `state_bucket_name` --> Name of the state bucket. Later referred as `BUCKET_NAME_HERE`.
   2. `sa_email` --> Email for the Service Account (used to configure WIF in the CI/CD pipeline).
   3. `workload_id_provider_name` --> ID of the WIF provider (used to configure WIF in the CI/CD pipeline).
7. Ensure the `backend.tf` file for your other Terraform stacks is pointing to the correct prefix (non-colliding prefixes).
8. Move into any of your other Terraform stacks to configure the state bucket.
9. Configure the state bucket by doing the following: `terraform init -backend-config "bucket=BUCKET_NAME_HERE"`.

### How to structure it?

We've included some template folders for Terraform `terraform/resources--[GROUP NAME]`. The idea is that you can group different resources that are correlated into the different stacks. Each of those stacks will have a specific `backend.tf` file with the following structure:
```hcl
terraform {
  backend "gcs" {
    prefix = "state--[GROUP NAME]"
  }
}
```

This ensures there's not a competition across stacks for the same state, leading to issues.

## Linters

We have included the following linters configured:
- `Flake8` --> Configuration at `.flake8`
- `Black` --> Configuration at `pyproject.toml`
- `SQLFluff` --> Configuration at `pyproject.toml`

Please ensure you are using them during your development, so that we ensure styling is consistent.

To prepare for the linters, please ensure you run the following command (from the root of the repository) to install all the dependencies:
```
source config.dst && pipenv install --dev
```

## Pre-Commit Hooks

To have pre-commit hooks, we use `Husky`. This will ensure that before you get to commit anything, you are working with the expected styling.

Please ensure that you delete any pre-commit rules that don't apply to your stack. For example, if you are not working with SQL in this repository, you should delete the `sqlfluff` part of the pre-commit hooks.