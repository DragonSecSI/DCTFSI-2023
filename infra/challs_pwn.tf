module "chall_pwn_vun" {
  source = "./modules/challs/pwn/"
  count = 1

  name = "vun"
  ip   = azurerm_public_ip.challs_pwn.ip_address
  port = 13370

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/vun:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name
}
