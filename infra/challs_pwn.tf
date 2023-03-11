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

module "chall_pwn_casino" {
  source = "./modules/challs/pwn/"
  count = 1

  name = "casino"
  ip   = azurerm_public_ip.challs_pwn.ip_address
  port = 13371

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/casino:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name
}

module "chall_pwn_xoxo" {
  source = "./modules/challs/pwn/"
  count = 1

  name = "xoxo"
  ip   = azurerm_public_ip.challs_pwn.ip_address
  port = 13372

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/xoxo:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name
}

module "chall_pwn_shellstraction" {
  source = "./modules/challs/pwn/"
  count = 1

  name = "shellstraction"
  ip   = azurerm_public_ip.challs_pwn.ip_address
  port = 13373

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/shellstraction:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name
}

module "chall_pwn_rsa" {
  source = "./modules/challs/pwn/"
  count = 1

  name = "rsa"
  ip   = azurerm_public_ip.challs_pwn.ip_address
  port = 13374

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/rsa:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name
}

module "chall_pwn_amazeing" {
  source = "./modules/challs/pwn/"
  count = 1

  name = "amazeing"
  ip   = azurerm_public_ip.challs_pwn.ip_address
  port = 13375

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/amazeing:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name
}

module "chall_pwn_pthread" {
  source = "./modules/challs/pwn/"
  count = 1

  name = "pthread"
  ip   = azurerm_public_ip.challs_pwn.ip_address
  port = 13376

  k8s_cpu_limits = "600m"
  k8s_memory_limits = "1024Mi"
  k8s_cpu_requests = "300m"
  k8s_memory_requests = "512Mi"

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/pthread:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name
}
