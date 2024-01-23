data "aws_ec2_instance_type" "all" {
  for_each      = var.node_groups
  instance_type = each.value["instance_type"]
}

locals {
  default_node_groups = {
    default = {
      name           = "small-cpu-workers"
      instance_types = ["t3.small"]
      ami_type       = "AL2_x86_64"
      min_size       = 1
      max_size       = 3
      desired_size   = 1

      tags = {
        "node.kubernetes.io/instance-type"                = "t3.small"
        "k8s.io/cluster-autoscaler/enabled"               = "true"
        "k8s.io/cluster-autoscaler/${local.cluster_name}" = "owned"
      }
    }
  }
  requested_node_groups = {
    for node_group_name, node_group_config in var.node_groups :
    node_group_name => {
      name           = "${node_group_name}"
      instance_types = [node_group_config["instance_type"]]
      ami_type       = tolist(data.aws_ec2_instance_type.all[node_group_name].gpus)[0]["count"] > 0 ? "AL2_x86_64_GPU" : "AL2_x86_64"
      min_size       = 0
      max_size       = node_group_config["max_count"]
      desired_size   = 0
      tags = merge(
        {
          "node.kubernetes.io/instance-type"                = node_group_config["instance_type"]
          "k8s.io/cluster-autoscaler/enabled"               = "true"
          "k8s.io/cluster-autoscaler/${local.cluster_name}" = "owned"
        },
        length(data.aws_ec2_instance_type.all[node_group_name].gpus) > 0 ? {
          "k8s.io/cluster-autoscaler/node-template/label/nvidia.com/gpu"                   = "true"
          "k8s.io/cluster-autoscaler/node-template/taint/nvidia.com/gpu"                   = "true"
          "k8s.io/cluster-autoscaler/node-template/label/node.kubernetes.io/instance-type" = node_group_config["instance_type"]
          "k8s.io/cluster-autoscaler/node-template/resources/nvidia.com/gpu"               = tolist(data.aws_ec2_instance_type.all[node_group_name].gpus)[0]["count"]
          "k8s.io/cluster-autoscaler/node-template/resources/cpu"                          = data.aws_ec2_instance_type.all[node_group_name].default_vcpus
        } : {}
      )
      taints = length(tolist(data.aws_ec2_instance_type.all[node_group_name].gpus)) > 0 ? [
        {
          key    = "nvidia.com/gpu"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      ] : []
      block_device_mappings = length(tolist(data.aws_ec2_instance_type.all[node_group_name].gpus)) > 0 ? {
        root = {
          device_name = "/dev/xvda"
          ebs = {
            volume_size = 64
          }
        }
      } : {}
      labels = merge(
        {
          "node.kubernetes.io/instance-type" = node_group_config["instance_type"]
          }, length(tolist(data.aws_ec2_instance_type.all[node_group_name].gpus)) > 0 ? {
          "nvidia.com/gpu" = "true"
        } : {}
      )
    }
  }
}

resource "aws_iam_policy" "autoscaling" {
  count       = var.eks_cluster_id != "" ? 1 : 0
  name        = "autoscaling-iam-policy-${var.eks_cluster_id}"
  description = ""

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "autoscaling:DescribeAutoScalingGroups",
          "autoscaling:DescribeAutoScalingInstances",
          "autoscaling:DescribeLaunchConfigurations",
          "autoscaling:DescribeScalingActivities",
          "autoscaling:DescribeTags",
          "ec2:DescribeInstanceTypes",
          "ec2:DescribeLaunchTemplateVersions"
        ],
        Resource = ["*"]
      },
      {
        Effect = "Allow",
        Action = [
          "autoscaling:SetDesiredCapacity",
          "autoscaling:TerminateInstanceInAutoScalingGroup",
          "ec2:DescribeImages",
          "ec2:GetInstanceTypesFromInstanceRequirements",
          "eks:DescribeNodegroup"
        ],
        Resource = ["*"]
      }
    ]
  })
}


module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  count   = local.create_eks_cluster ? 1 : 0
  version = "19.5.1"

  cluster_name    = local.cluster_name
  cluster_version = "1.24"

  vpc_id                         = module.vpc[0].vpc_id
  subnet_ids                     = module.vpc[0].private_subnets
  cluster_endpoint_public_access = true

  eks_managed_node_group_defaults = {
    iam_role_additional_policies = {
      "autoscaler" : aws_iam_policy.autoscaling[0].arn
    }
  }

  eks_managed_node_groups = merge(local.default_node_groups, local.requested_node_groups)

  node_security_group_name            = "${local.cluster_name}-node-security-group"
  node_security_group_use_name_prefix = true
  node_security_group_additional_rules = {
    fsx_main = {
      description = "allow lust traffic between fsx for lustre file servers, and servers and clients"
      from_port   = 988
      to_port     = 988
      protocol    = "tcp"
      type        = "ingress"
      cidr_blocks = ["0.0.0.0/0"]
    }
    fsx_extra = {
      description = "lustre traffic between fsx servers, servers and clients"
      from_port   = 1018
      to_port     = 1023
      protocol    = "tcp"
      type        = "ingress"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}

resource "helm_release" "k8s-device-plugin" {
  count      = local.create_eks_cluster ? 1 : 0
  name       = "k8s-device-plugin"
  repository = "https://nvidia.github.io/k8s-device-plugin"
  chart      = "nvidia-device-plugin"
  version    = "0.6.0"
  namespace  = "kube-system"
}

resource "aws_iam_role_policy_attachment" "nodes_fsx_access" {
  for_each   = local.create_eks_cluster ? module.eks[0].eks_managed_node_groups : {}
  role       = each.value.iam_role_name
  policy_arn = "arn:aws:iam::aws:policy/AmazonFSxFullAccess"

  depends_on = [module.eks[0]]
}

data "aws_eks_cluster_auth" "komodo" {
  count = local.create_eks_cluster ? 1 : 0
  name  = module.eks[0].cluster_name
}

provider "helm" {
  kubernetes {
    host                   = local.create_eks_cluster ? module.eks[0].cluster_endpoint : ""
    cluster_ca_certificate = local.create_eks_cluster ? base64decode(module.eks[0].cluster_certificate_authority_data) : ""
    token                  = local.create_eks_cluster ? data.aws_eks_cluster_auth.komodo[0].token : ""
  }
}

data "aws_region" "current" {}

resource "helm_release" "cluster_autoscaler" {
  count      = local.create_eks_cluster ? 1 : 0
  name       = "cluster-autoscaler"
  repository = "https://kubernetes.github.io/autoscaler"
  chart      = "cluster-autoscaler"

  set {
    name  = "autoDiscovery.clusterName"
    value = local.cluster_name
  }

  set {
    name  = "awsRegion"
    value = data.aws_region.current.name
  }
}
