resource "aws_ecr_repository" "komodo_overlays" {
  name                 = "komodo-overlays"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = false
  }
}
