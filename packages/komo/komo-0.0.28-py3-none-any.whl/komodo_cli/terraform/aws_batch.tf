locals {
  create_aws_batch = var.create_aws_batch && length(keys(var.aws_batch_compute_environments)) > 0
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_subnet" "default" {
  for_each = toset(data.aws_subnets.default.ids)
  id       = each.value
}

data "aws_security_group" "default" {
  count  = 1
  name   = "default"
  vpc_id = data.aws_vpc.default.id
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id       = data.aws_vpc.default.id
  service_name = "com.amazonaws.${var.aws_region}.s3"
}

resource "aws_security_group_rule" "allow_self_egress" {
  type                     = "egress"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "all"
  source_security_group_id = data.aws_security_group.default[0].id
  security_group_id        = data.aws_security_group.default[0].id
}

resource "aws_security_group_rule" "allow_ssh" {
  type                     = "ingress"
  from_port                = 22
  to_port                  = 22
  protocol                 = "TCP"
  cidr_blocks              = ["0.0.0.0/0"]
  security_group_id        = data.aws_security_group.default[0].id
}

resource "aws_eip" "komodo_batch_nat_gateway" {
  domain = "vpc"
  tags = {
    "Name" = "komodo-batch-nat-gateway"
  }
}

resource "aws_nat_gateway" "komodo_batch" {
  connectivity_type = "public"
  allocation_id     = aws_eip.komodo_batch_nat_gateway.allocation_id
  subnet_id         = local.original_vpc_subnets[0].id

  tags = {
    Name = "komodo-batch-nat-gateway"
  }
}

locals {
  original_vpc_subnets = [for s in data.aws_subnet.default: s if s.map_public_ip_on_launch]
}

resource "aws_subnet" "komodo_batch_private_subnets" {
  count = length(data.aws_availability_zones.available.names)
  vpc_id     = data.aws_vpc.default.id
  cidr_block = "172.31.${
    max(
      [
        for s in local.original_vpc_subnets :
        tonumber(
          split(
            ".",
            s.cidr_block
          )[2]
        ) + 16 + 16 * count.index
      ]...
    )
  }.0/20"

  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "komodo-batch-private-subnet"
  }
}

resource "aws_route_table" "komodo_batch_private_route_table" {
  vpc_id = data.aws_vpc.default.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.komodo_batch.id
  }
}

resource "aws_route_table_association" "komodo_batch_private_subnets" {
  count       = length(aws_subnet.komodo_batch_private_subnets)
  subnet_id      = aws_subnet.komodo_batch_private_subnets[count.index].id
  route_table_id = aws_route_table.komodo_batch_private_route_table.id
}

resource "aws_vpc_endpoint_route_table_association" "komodo_s3_gateway_association" {
  route_table_id = aws_route_table.komodo_batch_private_route_table.id
  vpc_endpoint_id = "${aws_vpc_endpoint.s3.id}"
}

locals {
  // create compute environment for each var.aws_batch_instance_types
  compute_environments = {
    for compute_env_name, compute_env_config in var.aws_batch_compute_environments :
    compute_env_name => {
      name = replace("${local.batch_name}-${compute_env_name}-${compute_env_config.instance_type}", ".", "-")
      compute_resources = {
        type                = "EC2"
        allocation_strategy = "BEST_FIT_PROGRESSIVE"

        instance_role = aws_iam_instance_profile.batch_instance_profile[0].arn
        instance_type = [compute_env_config.instance_type]
        efa_network_interface_indexes = compute_env_config.instance_type == "p3dn.24xlarge" ? [0] : (compute_env_config.instance_type == "p4d.24xlarge" ? range(4) : (compute_env_config.instance_type == "p5.48xlarge" ? range(32) : []))

        desired_vcpus = compute_env_config.desired_vcpus
        min_vcpus     = compute_env_config.min_vcpus
        max_vcpus     = compute_env_config.max_vcpus

        ec2_key_pair   = aws_key_pair.komodo[0].id
        bid_percentage = null

        tags = {}

        ec2_configuration = {
          image_type = "ECS_AL2_NVIDIA"
        }

        security_group_ids = [data.aws_security_group.default[0].id]
        subnets = [
          for subnet in aws_subnet.komodo_batch_private_subnets :
          subnet.id
        ]
      }
    }
  }
  launch_templates = {
    for compute_env_name, compute_env_config in var.aws_batch_compute_environments :
    compute_env_name => {
      block_device_mappings = {
        device_name = "/dev/xvda"
      }

      ebs = {
        volume_size = compute_env_config.volume_size
        volume_type = "gp3"
      }
    }
  }
}

resource "aws_placement_group" "efa" {
  for_each = local.launch_templates
  name     = "efa-${each.key}"
  strategy = "cluster"
}

resource "aws_launch_template" "komodo_batch" {
  for_each = local.compute_environments

  block_device_mappings {
    device_name = local.launch_templates[each.key].block_device_mappings.device_name

    ebs {
      volume_size = local.launch_templates[each.key].ebs.volume_size
      volume_type = local.launch_templates[each.key].ebs.volume_type
    }
  }

  placement {
    group_name = aws_placement_group.efa[each.key].name
  }

  dynamic "network_interfaces" {
    for_each = toset(each.value.compute_resources.efa_network_interface_indexes)
    content {
      device_index = network_interfaces.key
      network_card_index = network_interfaces.key
      security_groups = each.value.compute_resources.security_group_ids
      interface_type = "efa"
    }
  }

  update_default_version = true
}


resource "aws_iam_role" "batch_instance_role" {
  count              = local.create_aws_batch ? 1 : 0
  name               = "${local.batch_name}-instance-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "batch_instance_role_policy_ecs" {
  count      = local.create_aws_batch ? 1 : 0
  role       = aws_iam_role.batch_instance_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_role_policy_attachment" "batch_instance_role_policy_ec2_connect" {
  count      = local.create_aws_batch ? 1 : 0
  role       = aws_iam_role.batch_instance_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/EC2InstanceConnect"
}

resource "aws_iam_policy" "batch_instance_role_policy_ec2_connect_custom" {
  count  = local.create_aws_batch ? 1 : 0
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ec2-instance-connect:SendSSHPublicKey",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "ec2:osuser": "ec2-user"
                }
            }
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "batch_instance_role_policy_ec2_connect_custom" {
  count      = local.create_aws_batch ? 1 : 0
  role       = aws_iam_role.batch_instance_role[0].name
  policy_arn = aws_iam_policy.batch_instance_role_policy_ec2_connect_custom[0].arn
}

resource "aws_iam_role_policy_attachment" "batch_isntance_role_full_s3_access" {
  count      = local.create_aws_batch ? 1 : 0
  role       = aws_iam_role.batch_instance_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_instance_profile" "batch_instance_profile" {
  count = local.create_aws_batch ? 1 : 0
  name  = "${local.batch_name}-instance-profile"
  role  = aws_iam_role.batch_instance_role[0].name
}

data "aws_iam_role" "batch_service_role" {
  name = "AWSServiceRoleForBatch"
}

resource "aws_batch_compute_environment" "komodo" {
  for_each                 = local.compute_environments
  compute_environment_name = each.value.name
  type                     = "MANAGED"
  service_role             = data.aws_iam_role.batch_service_role.arn

  compute_resources {
    type                = each.value.compute_resources.type
    allocation_strategy = each.value.compute_resources.allocation_strategy

    instance_role  = each.value.compute_resources.instance_role
    instance_type  = each.value.compute_resources.instance_type
    min_vcpus      = each.value.compute_resources.min_vcpus
    max_vcpus      = each.value.compute_resources.max_vcpus
    ec2_key_pair   = each.value.compute_resources.ec2_key_pair
    bid_percentage = each.value.compute_resources.bid_percentage

    tags = {}

    ec2_configuration {
      image_type = each.value.compute_resources.ec2_configuration.image_type
    }

    launch_template {
      launch_template_id = aws_launch_template.komodo_batch[each.key].id
    }

    # only define security groups if the instance doesn't contain efa devices, since those devices will define security groups,
    # and those will conflict with these
    security_group_ids = length(each.value.compute_resources.efa_network_interface_indexes) > 0 ? null : each.value.compute_resources.security_group_ids

    subnets            = each.value.compute_resources.subnets
  }
}

resource "aws_batch_job_queue" "komodo" {
  for_each = local.compute_environments
  name     = "${local.batch_name}-${each.key}-queue"
  state    = "ENABLED"
  priority = 1
  compute_environments = [
    aws_batch_compute_environment.komodo[each.key].arn
  ]
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true


  filter {
    name   = "owner-alias"
    values = ["amazon"]
  }


  filter {
    name   = "name"
    values = ["amzn2-ami-hvm*"]
  }
}

resource "aws_instance" "batch_bastion" {
  count                       = local.create_aws_batch ? 1 : 0
  ami                         = data.aws_ami.amazon_linux_2.id
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  key_name                    = aws_key_pair.komodo[0].id
  subnet_id                   = local.original_vpc_subnets[0].id
  vpc_security_group_ids      = [data.aws_security_group.default[0].id]

  tags = {
    Name = "komodo-batch-${var.aws_batch_name}-bastion"
  }
}
