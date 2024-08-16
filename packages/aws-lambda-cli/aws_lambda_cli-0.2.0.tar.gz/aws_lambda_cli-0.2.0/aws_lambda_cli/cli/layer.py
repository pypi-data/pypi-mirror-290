import logging

import click

from aws_lambda_cli.cli.root import cli

logger = logging.getLogger(__name__)


@cli.command("layer")
@click.option("--aws_s3_bucket", default=None)
@click.option("--aws_s3_key", default=None)
@click.argument("layer")
def layer_cli():
    """
    Build and optionally upload an AWS Lambda layer.

    Layer: The AWS layer to modify.
    """
