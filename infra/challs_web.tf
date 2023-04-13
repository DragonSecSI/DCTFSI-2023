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
