import os
import pathlib
import shutil
import sys
from typing import Optional

import click
import jinja2
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.commands.compute.utils import (
    SUPPORTED_COMPUTE_SERVICES, ensure_terraform_state_resources,
    get_compute_dir, get_vars, get_vars_filepath, print_clusters, run_cmd,
    update_vars)
from komodo_cli.utils import handle_errors


@click.command("create")
@click.option(
    "--compute-type",
    "-t",
    type=str,
    default="aws",
    help="The type of compute infrastructure type to create.",
)
@click.option(
    "--name",
    "-n",
    type=str,
    required=True,
    help="The name for the newly created compute infrastructure",
)
@click.option(
    "--aws-region",
    type=str,
    required=True,
    help="The AWS region to create the compute infrastructure in.",
)
@click.option(
    "--aws-profile",
    type=str,
    required=True,
    help="The AWS profile to use for creating the compute infrastructure.",
)
@click.option(
    "--manual-confirm",
    "-m",
    type=bool,
    is_flag=True,
    default=False,
    required=False,
    help="Manually confirm terraform plan.",
)
@click.pass_context
@handle_errors
def cmd_create(
    ctx: click.Context,
    compute_type: Optional[str],
    name: Optional[str],
    aws_region: Optional[str],
    aws_profile: Optional[str],
    manual_confirm: Optional[bool],
):
    """Create Komodo compute"""
    if compute_type not in SUPPORTED_COMPUTE_SERVICES:
        printing.error(
            f"Unsupported compute type {compute_type}. Supported compute types: {SUPPORTED_COMPUTE_SERVICES}",
            bold=True,
        )
        sys.exit(1)

    compute_dir = get_compute_dir()
    script_dir = f"{pathlib.Path(__file__).parent.resolve()}"
    if not os.path.exists(compute_dir):
        os.makedirs(compute_dir)
    tf_dir = os.path.abspath(os.path.join(script_dir, "..", "..", "terraform"))

    (
        terraform_state_bucket_name,
        terraform_state_lock_dynamodb_table_name,
    ) = ensure_terraform_state_resources(aws_profile)

    # generate providers.tf from template
    templateLoader = jinja2.FileSystemLoader(searchpath=tf_dir)
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "providers.jinja"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(
        aws_profile=aws_profile,
        terraform_state_bucket_name=terraform_state_bucket_name,
        terraform_state_lock_dynamodb_table_name=terraform_state_lock_dynamodb_table_name,
    )
    with open(os.path.join(tf_dir, "providers.tf"), "w") as f:
        f.write(outputText)

    shutil.copytree(
        tf_dir,
        compute_dir,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("*.jinja"),
    )

    cmd = ["terraform", f"-chdir={compute_dir}", "init"]
    exit_code, _, stderr = run_cmd(" ".join(cmd))
    if exit_code != 0:
        logger.error(stderr)
        printing.error(f"Error initializing terraform.", bold=True)
        exit(1)

    try:
        tf_vars = get_vars(no_exist_ok=True)
    except Exception as e:
        logger.error(e)
        printing.error(
            f"Error loading tf vars",
            bold=True,
        )
        sys.exit(1)

    tf_vars["aws_region"] = aws_region
    tf_vars["aws_profile"] = aws_profile

    if compute_type == "eks":
        tf_vars[f"{compute_type}_cluster_id"] = name
    elif compute_type == "aws":
        tf_vars["create_aws_batch"] = True
        tf_vars["aws_batch_name"] = name

    update_vars(tf_vars)

    cmd = [
        "terraform",
        f"-chdir={compute_dir}",
        "apply",
    ]
    if not manual_confirm:
        cmd.append("-auto-approve")
    cmd.append(f"-var-file={get_vars_filepath()}")

    exit_code, _, stderr = run_cmd(" ".join(cmd))

    if exit_code != 0:
        logger.error(stderr)
        printing.error("Error creating compute", bold=True)
        printing.error(stderr)
        sys.exit(1)

    printing.success("Compute created successfully", bold=True)
    print_clusters()
    # TODO: post backend details to the server for backend config
