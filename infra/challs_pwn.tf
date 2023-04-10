#module "chall_pwn_template" {
#  source = "./modules/challs/pwn/"
#  count = 1
#
#  name = "template"
#  ip   = azurerm_public_ip.challs_pwn.ip_address
#  port = 13370
#
#  k8s_namespace       = "default"
#  k8s_image           = "dctf23.azurecr.io/challs/template:latest"
#  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name
#}
