"""
Utility functions for working with git
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

import typer

import epics_containers_cli.globals as globals
import epics_containers_cli.shell as shell
from epics_containers_cli.logging import log
from epics_containers_cli.shell import check_beamline_repo
from epics_containers_cli.utils import chdir


def get_image_name(
    repo: str,
    arch: globals.Architecture = globals.Architecture.linux,
    target: str = "developer",
    suffix: Optional[str] = None,
) -> str:
    if suffix is None:
        suffix = "-{arch}-{target}"
    registry = repo2registry(repo).lower()
    img_suffix = suffix.format(repo=repo, arch=arch, target=target, registry=registry)

    image = f"{registry}{img_suffix}"
    log.info("repo = %s image  = %s", repo, image)
    return image


def get_git_name(folder: Path = Path(".")) -> Tuple[str, Path]:
    """
    work out the git repo name and top level folder for a local clone
    """
    os.chdir(folder)
    path = str(shell.run_command("git rev-parse --show-toplevel", interactive=False))
    git_root = Path(path.strip())

    remotes = str(shell.run_command("git remote -v", interactive=False))
    log.debug(f"remotes = {remotes}")

    matches = re.findall(r"((?:(?:git@)|(?:http[s]+:\/\/)).*) (?:.fetch.)", remotes)

    if len(matches) > 0:
        repo_name = str(matches[0])
    else:
        log.error(f"folder {folder.absolute()} cannot parse repo name {remotes}")
        raise typer.Exit(1)

    log.debug(f"repo_name = {repo_name}, git_root = {git_root}")
    return repo_name, git_root


# work out what the registry name is for a given repo remote e.g.
def repo2registry(repo_name: str) -> str:
    """convert a repo name to the related a container registry name"""

    # First try matching using the regex mappings environment variable
    registry = ""
    # remove .git suffix because regexes are hard to make with optional suffix
    # not all git remotes have it for some reason
    repo_name = repo_name.removesuffix(".git")

    for mapping in globals.EC_REGISTRY_MAPPING_REGEX.split("\n"):
        if mapping == "":
            continue
        regex, replacement = mapping.split(" ")
        log.debug("regex = %s replacement = %s", regex, replacement)
        match = re.match(regex, repo_name)
        if match is not None:
            registry = match.expand(replacement)
            break

    if registry:
        return registry

    # Now try matching using the simple mappings environment variable.
    # Here automatically add the organization name to the image root URL
    log.debug("extracting fields from repo name %s", repo_name)

    match_git = re.match(r"git@([^:]*):(.*)\/(.*)", repo_name)
    match_http = re.match(r"https:\/\/([^\/]*)\/([^\/]*)\/([^\/]*)", repo_name)
    for match in [match_git, match_http]:
        if match is not None:
            source_reg, org, repo = match.groups()
            break
    else:
        log.error(f"repo {repo_name} is not a valid git remote")
        raise typer.Exit(1)

    log.debug("source_reg = %s org = %s repo = %s", source_reg, org, repo)

    for mapping in globals.EC_REGISTRY_MAPPING.split():
        if mapping.split("=")[0] == source_reg:
            registry = mapping.split("=")[1]
            registry = f"{registry}/{org}/{repo}"
            break
    else:
        log.error(f"repo {repo_name} does not match any registry mapping")
        log.error("please update the environment variable EC_REGISTRY_MAPPING")
        raise typer.Exit(1)

    return registry


def create_ioc_graph(beamline_repo: str, folder: Path) -> Dict:
    """
    return a dictionary of the available IOCs (by discovering the children
    to the iocs/ folder in the beamline repo) as well as a list of the corresponing
    available versions for each IOC (by discovering the tags in the beamline repo at
    which changes to the instance were made since the last tag) and the respective
    list of available versions
    """
    ioc_graph = {}

    check_beamline_repo(beamline_repo)
    shell.run_command(f"git clone {beamline_repo} {folder}", interactive=False)
    path_list = os.listdir(os.path.join(folder, "iocs"))
    ioc_list = [
        path for path in path_list if os.path.isdir(os.path.join(folder, "iocs", path))
    ]

    with chdir(folder):  # From python 3.11 can use contextlib.chdir(folder)
        for ioc_name in ioc_list:
            ioc_name = Path(ioc_name).name
            result = str(shell.run_command("git tag", interactive=False))
            log.debug(f"checking these tags for changes in the instance: {result}")

            version_list = []
            tags = result.split("\n")

            for tag in tags:
                if tag == "":
                    continue
                cmd = f"git diff --name-only {tag} {tag}^"
                result = str(shell.run_command(cmd, interactive=False))
                if ioc_name in result:
                    version_list.append(tag)

            if not version_list:
                # also look to see if the first tag was when the instance was created
                cmd = f"git diff --name-only {tags[0]} $(git hash-object -t tree /dev/null)"
                result = str(shell.run_command(cmd, interactive=False))
                if ioc_name in result:
                    version_list.append(tags[0])

            ioc_graph[ioc_name] = version_list

    return ioc_graph
