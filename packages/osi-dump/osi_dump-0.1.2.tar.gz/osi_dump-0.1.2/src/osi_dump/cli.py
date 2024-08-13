import logging

import os

from pathlib import Path

import typer

from typing_extensions import Annotated

app = typer.Typer()


from osi_dump.batch_handler.volume_batch_handler import VolumeBatchHandler
from osi_dump.os_connection.get_connections import get_connections


from osi_dump.batch_handler import (
    InstanceBatchHandler,
    ProjectBatchHandler,
    HypervisorBatchHandler,
    FloatingIPBatchHandler,
)


from osi_dump import util


def _instance(connections, output_path: str):
    instance_batch_handler = InstanceBatchHandler()

    instance_batch_handler.add_importer_exporter_from_openstack_connections(
        connections, output_file=output_path
    )

    instance_batch_handler.process()


def _floating_ip(connections, output_path: str):
    floating_ip_batch_handler = FloatingIPBatchHandler()

    floating_ip_batch_handler.add_importer_exporter_from_openstack_connections(
        connections, output_file=output_path
    )

    floating_ip_batch_handler.process()


def _volume(connections, output_path: str):
    volume_batch_handler = VolumeBatchHandler()

    volume_batch_handler.add_importer_exporter_from_openstack_connections(
        connections, output_file=output_path
    )

    volume_batch_handler.process()


def _project(connections, output_path: str):
    project_batch_handler = ProjectBatchHandler()

    project_batch_handler.add_importer_exporter_from_openstack_connections(
        connections, output_file=output_path
    )

    project_batch_handler.process()


def _hypervisor(connections, output_path: str):
    hypervisor_batch_handler = HypervisorBatchHandler()

    hypervisor_batch_handler.add_importer_exporter_from_openstack_connections(
        connections, output_file=output_path
    )

    hypervisor_batch_handler.process()


def inner_main(file_path: str, output_path: str):

    logger = logging.getLogger(__name__)

    connections = get_connections(file_path=file_path)

    _instance(connections=connections, output_path=output_path)

    _floating_ip(connections=connections, output_path=output_path)

    _volume(connections=connections, output_path=output_path)

    _hypervisor(connections=connections, output_path=output_path)

    _project(connections=connections, output_path=output_path)

    util.excel_autosize_column(output_path)

    util.excel_sort_sheet(output_path)

    logger.info(
        f"Exported OpenStack information to file: {os.path.abspath(output_path)}"
    )


def main(
    file_path: Annotated[
        Path,
        typer.Argument(
            help=(
                """
            Path of the file containing OpenStack authentication information.

            The expected JSON file format is as follows:

\b
[
    {
	"auth_url": "string",
	"project_name": "string",
	"username": "string",
	"password": "string",
	"user_domain_name": "string",
	"project_domain_name": "string"
    }
]
            """
            )
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="""
\b
Path of the output file, will override if file already exists
             
                """
        ),
    ] = "output.xlsx",
):
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger(__name__)

    if util.validate_dir_path(file_path=output_path) is False:
        logger.error(f"Invalid path: {output_path}, folder does not exist.")
        raise typer.Exit(1)

    inner_main(file_path=file_path, output_path=output_path)


app.command()(main)

if __name__ == "__main__":
    app()
