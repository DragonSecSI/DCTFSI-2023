variable "registration_email" {
  description = "Let's encrypt registration email"
  type = string
  nullable = false
}

variable "common_name" {
  description = "Certificate common name"
  type = string
  nullable = false
}

variable "alternative_names" {
  description = "Additional certificate alternative names"
  type = list
  default = []
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token"
  type = string
  sensitive = true
  nullable = false
}
