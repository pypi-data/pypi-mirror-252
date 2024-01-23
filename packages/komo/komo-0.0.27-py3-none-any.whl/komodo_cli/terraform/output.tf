output "eks_cluster_endpoint" {
  value = local.create_eks_cluster ? module.eks[0].cluster_endpoint : ""
}

output "eks_cluster_bearer_token" {
  value     = local.create_eks_cluster ? module.komodo_manifests.cluster_bearer_token : ""
  sensitive = true
}

output "eks_cluster_id" {
  value = local.create_eks_cluster ? module.eks[0].cluster_id : ""
}

output "eks_cluster_komodo_executor_role_arn" {
  value = local.create_eks_cluster ? module.komodo_manifests.komodo_executor_iam_role_arn : ""
}

output "eks_managed_node_groups" {
  value = local.create_eks_cluster ? module.eks[0].eks_managed_node_groups : {}
}

output "awsbatch_id" {
  value = var.aws_batch_name
}

locals {
  output_awsbatch_compute_environment_arns = [
    for abce in aws_batch_compute_environment.komodo :
    abce.arn
  ]
  output_aws_batch_queue_arns = [
    for abq in aws_batch_job_queue.komodo :
    abq.arn
  ]
}

output "awsbatch_compute_environment_arns" {
  value = local.create_aws_batch ? local.output_awsbatch_compute_environment_arns : []
}

output "awsbatch_queue_arns" {
  value = local.create_aws_batch ? local.output_aws_batch_queue_arns : []
}

output "awsbatch_bastion_ip_address" {
  value = local.create_aws_batch ? aws_instance.batch_bastion[0].public_ip : ""
}

output "komodo_ssh_key_path" {
  value = local.bastion_ssh_key_path
}

output "container_repository_url" {
  value = aws_ecr_repository.komodo_overlays.repository_url
}
