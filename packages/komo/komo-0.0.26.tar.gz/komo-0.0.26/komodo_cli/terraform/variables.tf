variable "aws_profile" {
  description = "AWS profile"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "eks_cluster_id" {
  description = "ID of the EKS cluster"
  type        = string
  default     = ""
}

variable "fsx_s3_buckets" {
  description = "List of S3 buckets to create FSx resources for"
  type        = list(string)
  default     = []
}

variable "node_groups" {
  description = "Map of user-defined node groups"
  type = map(object({
    instance_type = string
    max_count     = number
  }))
  default = {}
}

variable "create_aws_batch" {
  description = "Whether to create AWS Batch resources"
  type        = bool
  default     = false
}

variable "aws_batch_name" {
  description = "Name of the AWS Batch compute environment"
  type        = string
  default     = ""
}

variable "aws_batch_compute_environments" {
  description = "Map of user-defined compute environments"
  type = map(object({
    instance_type = string
    desired_vcpus = number
    min_vcpus     = number
    max_vcpus     = number
    volume_size   = number
  }))
  default = {}
}
