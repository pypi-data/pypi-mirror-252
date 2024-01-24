"""
utility functions
"""

import contextlib
import os
import re
import shutil
from pathlib import Path
from typing import Optional

import typer

import epics_containers_cli.globals as globals
from epics_containers_cli.logging import log


def get_instance_image_name(ioc_instance: Path, tag: Optional[str] = None) -> str:
    ioc_instance = ioc_instance.resolve()
    values = ioc_instance / "values.yaml"
    if not values.exists():
        log.error(f"values.yaml not found in {ioc_instance}")
        raise typer.Exit(1)

    values_text = values.read_text()
    matches = re.findall(r"image: (.*):(.*)", values_text)
    if len(matches) == 1:
        tag = tag or matches[0][1]
        image = matches[0][0] + f":{tag}"
    else:
        log.error(f"image tag definition not found in {values}")
        raise typer.Exit(1)

    return image


def check_ioc_instance_path(ioc_path: Path):
    """
    verify that the ioc instance path is valid
    """
    ioc_path = ioc_path.absolute()
    ioc_name = ioc_path.name.lower()

    log.info(f"checking IOC instance {ioc_name} at {ioc_path}")
    if ioc_path.is_dir():
        if (
            not (ioc_path / "values.yaml").exists()
            or not (ioc_path / globals.CONFIG_FOLDER).is_dir()
        ):
            log.error("IOC instance requires values.yaml and config")
            raise typer.Exit(1)
    else:
        log.error(f"IOC instance path {ioc_path} does not exist")
        raise typer.Exit(1)

    return ioc_name, ioc_path


def generic_ioc_from_image(image_name: str) -> str:
    """
    return the generic IOC name from an image name
    """
    match = re.findall(r".*\/(.*)-.*-(?:runtime|developer)", image_name)
    if not match:
        log.error(f"cannot extract generic IOC name from {image_name}")
        raise typer.Exit(1)

    return match[0]


def drop_ioc_path(raw_input: str):
    """
    Extracts the IOC name if is a path through ioc
    """
    match = re.findall(
        r"iocs\/(.*?)(?:/|\s|$)", raw_input
    )  # https://regex101.com/r/L3GUvk/1
    if not match:
        return raw_input

    extracted_ioc = match[0]
    typer.echo(f"Extracted ioc name {extracted_ioc} from input: {raw_input}")

    return extracted_ioc


@contextlib.contextmanager
def chdir(path):
    """
    A simple wrapper around chdir(), it changes the current working directory
    upon entering and restores the old one on exit.
    """
    curdir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(curdir)


def cleanup_temp(folder_path: Path) -> None:
    # keep the tmp folder if debug is enabled for inspection
    if not globals.EC_DEBUG:
        shutil.rmtree(folder_path, ignore_errors=True)
    else:
        log.debug(f"Temporary directory {folder_path} retained")


def normalize_tag(tag: str) -> str:
    """
    normalize a tag to be lowercase and replace any '/'
    this is needed in CI because dependabot tags
    """
    tag = tag.lower()
    tag = tag.replace("/", "-")
    return tag
