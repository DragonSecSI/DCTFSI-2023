module "chall_web_tmnt" {
  source = "./modules/challs/web/"
  count = 1

  name     = "tmnt"
  hostname = "tmnt.dctf.si"
  tls      = kubernetes_secret.dctf-wildcard.metadata.0.name

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/timely-manner:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name

  cloudflare_name    = "tmnt"
  cloudflare_zone_id = data.cloudflare_zone.dctf.id
  cloudflare_proxied = false
  cloudflare_ttl     = 1
}

module "chall_web_blog" {
  source = "./modules/challs/web-blog/"
  count = 1

  name     = "blog"
  hostname = "blog.dctf.si"
  tls      = kubernetes_secret.dctf-blog.metadata.0.name

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/yet-another-blog:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name

  cloudflare_name    = "blog"
  cloudflare_zone_id = data.cloudflare_zone.dctf.id
  cloudflare_proxied = false
  cloudflare_ttl     = 1
}

module "chall_web_101" {
  source = "./modules/challs/web/"
  count = 1

  name     = "web-101"
  hostname = "web-101.dctf.si"
  tls      = kubernetes_secret.dctf-wildcard.metadata.0.name

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/web-101:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name

  cloudflare_name    = "web-101"
  cloudflare_zone_id = data.cloudflare_zone.dctf.id
  cloudflare_proxied = false
  cloudflare_ttl     = 1
}

module "chall_web_sanitizer3000" {
  source = "./modules/challs/web-bot/"
  count = 1

  name     = "sanitizer3000"
  hostname = "sanitizer3000.dctf.si"
  tls      = kubernetes_secret.dctf-wildcard.metadata.0.name

  k8s_namespace       = "default"
  k8s_image           = "dctf23.azurecr.io/challs/sanitizer3000:latest"
  k8s_image_bot       = "dctf23.azurecr.io/challs/sanitizer3000-bot:latest"
  k8s_registry_secret = kubernetes_secret.registry_secret.metadata.0.name

  cloudflare_name    = "sanitizer3000"
  cloudflare_zone_id = data.cloudflare_zone.dctf.id
  cloudflare_proxied = false
  cloudflare_ttl     = 1
}
