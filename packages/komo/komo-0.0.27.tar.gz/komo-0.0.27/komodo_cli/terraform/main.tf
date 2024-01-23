locals {
  create_eks_cluster = var.eks_cluster_id != ""
  cluster_name       = "komodo-${var.eks_cluster_id}"
  batch_name         = "komodo-${var.aws_batch_name}"
}

module "komodo_manifests" {
  source                         = "./komodo_manifests"
  aws_profile                    = var.aws_profile
  region                         = var.aws_region
  cluster_endpoint               = local.create_eks_cluster ? module.eks[0].cluster_endpoint : ""
  cluster_ca_data                = local.create_eks_cluster ? module.eks[0].cluster_certificate_authority_data : ""
  cluster_id                     = local.create_eks_cluster ? module.eks[0].cluster_name : ""
  cluster_node_security_group_id = local.create_eks_cluster ? module.eks[0].node_security_group_id : ""
  cluster_node_subnet_ids        = local.create_eks_cluster ? module.vpc[0].private_subnets : []
  fsx_s3_buckets                 = var.fsx_s3_buckets
}
