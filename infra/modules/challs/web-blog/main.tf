resource "kubernetes_ingress_v1" "ingress" {
  metadata {
    name = "web-${var.name}-ingress"
    namespace = var.k8s_namespace

    annotations = {
      "kubernetes.io/ingress.class" = "nginx"
    }
  }

  spec {
    rule {
      host = "${var.hostname}"
      http {
        path {
          backend {
            service {
              name = kubernetes_service_v1.service.metadata.0.name
              port {
                number = 8000
              }
            }
          }

          path = "/"
        }
      }
    }

    tls {
      secret_name = var.tls
    }
  }

  wait_for_load_balancer = true
}

resource "kubernetes_service_v1" "service" {
  metadata {
    name = "web-${var.name}-service"
    namespace = var.k8s_namespace
  }
  spec {
    selector = {
      app = kubernetes_deployment_v1.deployment.spec.0.template.0.metadata.0.labels.app
    }

    port {
      port        = 8000
      target_port = 8000
    }

    type = "ClusterIP"
  }
}

resource "kubernetes_deployment_v1" "deployment" {
  metadata {
    name = "web-${var.name}-deployment"
    namespace = var.k8s_namespace
    labels = {
      app = "${var.name}"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "${var.name}"
      }
    }

    template {
      metadata {
        labels = {
          app = "${var.name}"
        }
      }

      spec {
        container {
          image = "${var.k8s_image}"
          name  = "${var.name}"

          security_context {
            run_as_user     = 1337
            run_as_group    = 1337
            run_as_non_root = true
            capabilities {
              add = [
                "NET_BIND_SERVICE",
              ]
            }
          }

          resources {
            limits = {
              cpu    = "0.3"
              memory = "512Mi"
            }
            requests = {
              cpu    = "0.1"
              memory = "128Mi"
            }
          }

          volume_mount {
            name       = "certs"
            mount_path = "/secrets"
            read_only  = true
          }
        }

        image_pull_secrets {
          name = var.k8s_registry_secret
        }

        volume {
          name = "certs"
          secret {
            secret_name = var.tls
          }
        }
      }
    }
  }
}
