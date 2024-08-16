import os
import shutil
import sys
import tempfile

import click

from .cosmo_torrent import _md5_sum, data_path
from .vars import (
    COSMO_TORRENT_REMOTE_FOLDER,
    COSMO_TORRENT_SSH_SERVER,
    COSMO_TORRENT_SSH_PORT,
)


@click.command()
@click.argument("identifier")
def download(identifier):
    sys.exit(_download(identifier))


def _download(identifier):
    try:
        folder = data_path(identifier)
    except Exception as e:
        click.secho(f"error: {e}", fg="red")
        return 1
    click.secho("data available at", fg="green")
    click.secho(f"{folder}", fg="green")
    return 0


@click.command()
@click.option(
    "--identifier",
    help="data set identifier for later download",
    type=str,
    required=True,
)
@click.option(
    "--user",
    help="user name for scp to server",
    default=os.environ.get("USER"),
    show_default=True,
    type=str,
)
@click.option(
    "--force",
    help="overwrite existing dataset",
    is_flag=True,
)
@click.argument("folder")
def upload(identifier, user, folder, force):
    sys.exit(_upload(identifier, user, folder, force))


def _upload(
    identifier,
    user,
    folder,
    force,
    COSMO_TORRENT_SSH_SERVER=COSMO_TORRENT_SSH_SERVER,
    COSMO_TORRENT_SSH_PORT=COSMO_TORRENT_SSH_PORT,
    COSMO_TORRENT_REMOTE_FOLDER=COSMO_TORRENT_REMOTE_FOLDER,
):
    if not os.path.exists(folder):
        click.secho(f"folder {folder} does not exist", fg="red")
        return 1

    result = os.system(
        f"ssh -p {COSMO_TORRENT_SSH_PORT} -o StrictHostKeyChecking=no"
        f" {user}@{COSMO_TORRENT_SSH_SERVER}"
        f" ls {COSMO_TORRENT_REMOTE_FOLDER}/{identifier}.zip"
        " 2>/dev/null >/dev/null"
    )

    if result == 0 and not force:
        click.secho(
            "data set with identifier {identifier} exists already."
            " use --force to overwrite.",
            fg="red",
        )
        return 1

    prep_folder = tempfile.mkdtemp()
    click.secho("create archive", fg="green")
    shutil.make_archive(os.path.join(prep_folder, identifier), "zip", folder, ".")
    md5_sum = _md5_sum(os.path.join(prep_folder, identifier) + ".zip")
    click.secho("create md5 file", fg="green")
    with open(os.path.join(prep_folder, identifier) + ".md5", "w") as fh:
        fh.write(md5_sum)

    result = os.system(
        f"scp -P {COSMO_TORRENT_SSH_PORT} -o StrictHostKeyChecking=no"
        f" {prep_folder}/*"
        f" {user}@{COSMO_TORRENT_SSH_SERVER}:{COSMO_TORRENT_REMOTE_FOLDER}"
    )

    if result == 0:
        click.secho(f"uploaded files from {folder} to server", fg="green")
    else:
        click.secho(f"upload of {folder} to server failed", fg="red")
    return result
