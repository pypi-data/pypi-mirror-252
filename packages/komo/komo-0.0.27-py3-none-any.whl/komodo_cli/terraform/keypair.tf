locals {
  bastion_ssh_key_path = local.create_aws_batch ? abspath("${path.module}/../${aws_key_pair.komodo[0].key_name}") : ""
}

resource "tls_private_key" "komodo" {
  algorithm = "ED25519"
}

resource "aws_key_pair" "komodo" {
  count      = local.create_aws_batch ? 1 : 0
  key_name   = "komodo-ssh-key-${var.aws_batch_name}"
  public_key = tls_private_key.komodo.public_key_openssh
}

resource "local_sensitive_file" "this" {
  count    = local.create_aws_batch ? 1 : 0
  content  = tls_private_key.komodo.private_key_openssh
  filename = local.bastion_ssh_key_path
}
