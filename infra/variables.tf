# Cloudflare

variable "cloudflare_api_token" {
  description = "Cloudflare API token"
  type        = string
  sensitive   = true
  nullable    = false
}

# Config

variable "azure_resource_group_name" {}
variable "azure_resource_group_location" {}

variable "azure_k8s_vm_type" {}
variable "azure_k8s_auto_scaling" {}
variable "azure_k8s_nodes_count" {}
variable "azure_k8s_nodes_min_count" {}
variable "azure_k8s_nodes_max_count" {}

variable "azure_k8s_registry_secret" {
  description = "Docker registry secret"
  type        = string
  sensitive   = true
  nullable    = false
}
variable "azure_k8s_namespace" {}

variable "certificate_registration_email" {}
