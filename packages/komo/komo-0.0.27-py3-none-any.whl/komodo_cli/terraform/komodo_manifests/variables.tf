variable "aws_profile" {
  description = "AWS profile"
  type        = string
  default     = "komodo"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "cluster_id" {}

variable "cluster_endpoint" {}

variable "cluster_ca_data" {}

variable "cluster_node_security_group_id" {}

variable "cluster_node_subnet_ids" {}

variable "fsx_s3_buckets" {
  description = "List of S3 buckets to create FSx resources for"
  type        = list(string)
  default     = []
}
