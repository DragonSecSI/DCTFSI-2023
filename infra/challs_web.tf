#module "chall_web_template" {
#  source = "./modules/challs/web/"
#  count = 1
#
#  name     = "template"
#  hostname = "template.dctf.si"
#  tls      = kubernetes_secret.dctf-wildcard.metadata.0.name
#
#  k8s_namespace       = "default"
#  k8s_image           = "dctf23.azurecr.io/challs/template:latest"
#  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name
#
#  cloudflare_name    = "template"
#  cloudflare_zone_id = data.cloudflare_zone.dctf.id
#  cloudflare_proxied = false
#  cloudflare_ttl     = 1
#}
