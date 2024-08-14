variable "environment" {
  type        = string
  description = "Environment (prod/dev), default dev"
  default     = "dev"
}

variable "project_id" {
  type = string
}

variable "region" {
  type        = string
  description = "GCP region https://cloud.google.com/compute/docs/regions-zones default US"
  default     = "US"
}

variable "repo" {
  type        = string
  description = "Name of the repository in which the WIF is going to be used."
}