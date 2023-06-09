resource "azurerm_resource_group" "challs" {
  name     = var.azure_resource_group_name
  location = var.azure_resource_group_location
}

resource "azurerm_kubernetes_cluster" "k8s" {
  name                = "dctf"
  location            = azurerm_resource_group.challs.location
  resource_group_name = azurerm_resource_group.challs.name
  dns_prefix          = "dctf23"

  default_node_pool {
    name    = "default"
    vm_size = var.azure_k8s_vm_type

    enable_auto_scaling = var.azure_k8s_auto_scaling
    node_count          = var.azure_k8s_nodes_count
    min_count           = var.azure_k8s_nodes_min_count
    max_count           = var.azure_k8s_nodes_max_count
  }

  identity {
    type = "SystemAssigned"
  }

  lifecycle {
    ignore_changes = [
      oms_agent
    ]
  }
}

resource "azurerm_public_ip" "challs_pwn" {
  name                = "challs_pwn_public_ip"
  resource_group_name = "MC_${azurerm_resource_group.challs.name}_${azurerm_kubernetes_cluster.k8s.name}_${azurerm_resource_group.challs.location}"
  location            = azurerm_resource_group.challs.location
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_public_ip" "challs_web_path" {
  name                = "challs_web_path_public_ip"
  resource_group_name = "MC_${azurerm_resource_group.challs.name}_${azurerm_kubernetes_cluster.k8s.name}_${azurerm_resource_group.challs.location}"
  location            = azurerm_resource_group.challs.location
  allocation_method   = "Static"
  sku                 = "Standard"
}

module "nginx-controller" {
  source  = "terraform-iaac/nginx-controller/helm"
  version = "2.0.1"
}
