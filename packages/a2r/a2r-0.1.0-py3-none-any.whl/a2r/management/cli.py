import logging
from pathlib import Path

import click

import a2r
from a2r import settings
from a2r.core import cleaner
from a2r.core import md5
from a2r.core import safe_rm

logger = logging.getLogger("a2r")

verbose_option = click.option(
    "-d", "--debug", "DEBUG", is_flag=True, help="Enable debug mode."
)


@click.group()
@click.version_option(package_name="a2r")
def main():
    a2r.setup()


@main.command()
@click.option("-c", "--config", type=Path, required=True)
@click.option("--dry-run", is_flag=True, help="Dry run mode.")
@verbose_option
def rolling(config, dry_run, **kwargs):
    settings.configure(**kwargs)
    cleaner.start(config, dry_run)


@main.command()
@click.option("--keep", "path_to_keep", type=Path, required=True)
@click.option("--clean", "path_to_clean", type=Path, required=True)
@click.option(
    "-f",
    "--force",
    "force_mode",
    is_flag=True,
    default=False,
    help="Delete files without confirm request",
)
@click.option(
    "-d", "--dry-run", is_flag=True, default=False, help="Disable file removal"
)
@verbose_option
def saferm(
    path_to_keep: Path, path_to_clean: Path, force_mode: bool, dry_run: bool, **kwargs
):
    settings.configure(**kwargs)
    safe_rm.start(path_to_keep, path_to_clean, force_mode, dry_run)


@main.command()
@click.option("-p", "--path", "path", type=Path, required=True)
@verbose_option
def update_md5(path: Path, **kwargs):
    settings.configure(**kwargs)
    md5.update_dir_md5(path)


if __name__ == "__main__":
    main()
