terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.31.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = "1.14.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.24.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "2.10.1"
    }
  }
}


data "aws_eks_cluster_auth" "komodo" {
  count = var.cluster_id != "" ? 1 : 0
  name  = var.cluster_id
}

provider "kubectl" {
  host                   = var.cluster_endpoint
  cluster_ca_certificate = base64decode(var.cluster_ca_data)
  token                  = var.cluster_id != "" ? data.aws_eks_cluster_auth.komodo[0].token : ""
  load_config_file       = false
}

data "kubectl_path_documents" "manifests" {
  count   = var.cluster_id != "" ? 1 : 0
  pattern = "${path.module}/files/*.yaml"
}

resource "kubectl_manifest" "volcano" {
  for_each  = var.cluster_id != "" ? toset(data.kubectl_path_documents.manifests[0].documents) : toset([])
  yaml_body = each.value
}

provider "kubernetes" {
  host                   = var.cluster_endpoint
  cluster_ca_certificate = base64decode(var.cluster_ca_data)
  token                  = var.cluster_id != "" ? data.aws_eks_cluster_auth.komodo[0].token : ""
}

data "kubernetes_secret" "komodo_runner" {
  count = var.cluster_id != "" ? 1 : 0
  metadata {
    name = "komodo-runner-secret"
  }

  depends_on = [kubectl_manifest.volcano]
}

resource "aws_iam_policy" "fsx_iam_access" {
  count = var.cluster_id != "" ? 1 : 0
  name  = "fsx-iam-access-${var.cluster_id}"
  path  = "/"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iam:CreateServiceLinkedRole",
          "iam:AttachRolePolicy",
          "iam:PutRolePolicy"
        ]
        Resource = "arn:aws:iam::*:role/aws-service-role/s3.data-source.lustre.fsx.amazonaws.com/*"
      }
    ]
  })
}

resource "aws_iam_policy" "fsx_s3_access" {
  count = var.cluster_id != "" ? 1 : 0
  name  = "fsx-s3-access-${var.cluster_id}"
  path  = "/"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:Get*",
          "s3:List*",
          "s3:PutObject"
        ]
        Resource = ["arn:aws:s3:::*", "arn:aws:s3:::*/*"]
      }
    ]
  })
}

module "iam_eks_role" {
  count   = var.cluster_id != "" ? 1 : 0
  source  = "terraform-aws-modules/iam/aws//modules/iam-eks-role"
  version = "5.20.0"

  create_role           = true
  force_detach_policies = true
  max_session_duration  = 43200
  role_name             = "komodo-executor-${var.cluster_id}"

  cluster_service_accounts = {
    (var.cluster_id) = ["default:komodo-executor", "default:fsx-csi-node-sa", "default:fsx-csi-controller-sa"]
  }

  role_policy_arns = {
    AmazonEKS_CNI_Policy = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
    FSxFullAccess        = "arn:aws:iam::aws:policy/AmazonFSxFullAccess"
    FSxAccess            = aws_iam_policy.fsx_iam_access[0].arn
    FsxS3Access          = aws_iam_policy.fsx_s3_access[0].arn
  }

  assume_role_condition_test = "StringLike"

  depends_on = [kubectl_manifest.volcano, aws_iam_policy.fsx_iam_access, aws_iam_policy.fsx_s3_access]
}

resource "kubernetes_service_account" "komodo_executor" {
  count = var.cluster_id != "" ? 1 : 0
  metadata {
    name      = "komodo-executor"
    namespace = "default"
    annotations = {
      "eks.amazonaws.com/role-arn" = module.iam_eks_role[0].iam_role_arn
    }
  }

  # Associate the service account with the IAM role
  automount_service_account_token = true

  /* image_pull_secrets = ["your-docker-registry-secret-name"] # TODO */
}

// OUTPUTS
output "cluster_bearer_token" {
  value     = var.cluster_id != "" ? data.kubernetes_secret.komodo_runner[0].data["token"] : ""
  sensitive = true
}

output "komodo_executor_iam_role_arn" {
  value = var.cluster_id != "" ? module.iam_eks_role[0].iam_role_arn : ""
}

provider "helm" {
  kubernetes {
    host                   = var.cluster_endpoint
    cluster_ca_certificate = base64decode(var.cluster_ca_data)
    token                  = var.cluster_id != "" ? data.aws_eks_cluster_auth.komodo[0].token : ""
    /* load_config_file       = false */
  }
}

resource "null_resource" "download_chart" {
  count = var.cluster_id != "" ? 1 : 0
  provisioner "local-exec" {
    command = <<EOT
      if [ ! -d komodo_manifests/volcano ]; then
        rm -rf komodo_manifests/volcano
        git clone https://github.com/volcano-sh/volcano.git komodo_manifests/volcano
      fi
    EOT
  }
  triggers = {
    always_run = "${timestamp()}"
  }
}

resource "kubernetes_namespace" "volcano" {
  count = var.cluster_id != "" ? 1 : 0
  metadata {
    name = "volcano-system"
  }
}

resource "helm_release" "volcano" {
  count      = var.cluster_id != "" ? 1 : 0
  name       = "volcano"
  chart      = "komodo_manifests/volcano/installer/helm/chart/volcano"
  repository = "https://volcano-sh.github.io/charts"
  namespace  = "volcano-system"

  set {
    name  = "basic.image_tag_version"
    value = "v1.8.0"
  }
  depends_on = [null_resource.download_chart]
}

resource "helm_release" "fsx" {
  count = length(var.fsx_s3_buckets) > 0 ? 1 : 0
  name  = "aws-fsx-csi-driver"
  chart = "https://github.com/kubernetes-sigs/aws-fsx-csi-driver/releases/download/helm-chart-aws-fsx-csi-driver-1.6.0/aws-fsx-csi-driver-1.6.0.tgz"
  values = [<<YAML
controller:
  serviceAccount:
    annotations:
      eks.amazonaws.com/role-arn: ${module.iam_eks_role[0].iam_role_arn}
node:
  serviceAccount:
    annotations:
      eks.amazonaws.com/role-arn: ${module.iam_eks_role[0].iam_role_arn}
YAML
  ]
}

resource "kubernetes_storage_class_v1" "fsx" {
  for_each = toset(var.fsx_s3_buckets)

  metadata {
    name = "fsx-sc-${each.key}"
  }
  storage_provisioner = "fsx.csi.aws.com"
  parameters = {
    subnetId         = var.cluster_node_subnet_ids[0]
    securityGroupIds = var.cluster_node_security_group_id
    s3ImportPath     = "s3://${each.key}"
    s3ExportPath     = "s3://${each.key}/export"
    deploymentType   = "SCRATCH_2"
    /* autoImportPolicy         = "NEW_CHANGED_DELETED" */
    /* perUnitStorageThroughput = "200" */
  }
  mount_options       = ["flock"]
  volume_binding_mode = "WaitForFirstConsumer"
}

resource "kubernetes_persistent_volume_claim" "fsx_storage" {
  for_each = toset(var.fsx_s3_buckets)
  metadata {
    name = "fsx-claim-${each.key}"
  }
  wait_until_bound = false
  spec {
    access_modes       = ["ReadWriteMany"]
    storage_class_name = "fsx-sc-${each.key}"
    resources {
      requests = {
        storage = "1200Gi"
      }
    }
  }
}
