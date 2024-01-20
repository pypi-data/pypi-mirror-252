import os
import re
import requests
import datetime

from typing import TypedDict, List, Dict, Any, Iterator, Optional, Union, cast

from semantic_version import Version

from pibble.api.configuration import APIConfiguration
from pibble.util.files import load_yaml, load_json
from enfugue.util.misc import merge_into

__all__ = [
    "VersionDict",
    "check_make_directory",
    "check_make_directory_by_names",
    "get_local_installation_directory",
    "get_local_config_directory",
    "get_local_static_directory",
    "get_local_configuration",
    "get_version",
    "get_versions",
    "get_pending_versions",
    "find_file_in_directory",
    "find_files_in_directory"
]

class VersionDict(TypedDict):
    """
    The version dictionary.
    """
    version: Version
    release: datetime.date
    description: str

def get_local_installation_directory() -> str:
    """
    Gets where the local installation directory is (i.e. where the package data files are,
    either in ../site-packages/enfugue on a python installation, or ${ROOT}/enfugue in a
    precompiled package
    """
    here = os.path.dirname(os.path.abspath(__file__))
    while not os.path.basename(here) == "enfugue":
        here = os.path.abspath(os.path.join(here, "../"))
        if here == "/":
            raise IOError("Couldn't find installation directory.")
    return here

def get_local_config_directory() -> str:
    """
    Gets where the local configuration directory is.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isdir(os.path.join(here, "config")):
        here = os.path.abspath(os.path.join(here, "../"))
        if here == "/":
            raise IOError("Couldn't find config directory.")
    return os.path.join(here, "config")

def get_local_static_directory() -> str:
    """
    Gets where the local static directory is.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isdir(os.path.join(here, "static")):
        here = os.path.abspath(os.path.join(here, "../"))
        if here == "/":
            raise IOError("Couldn't find static directory.")
    return os.path.join(here, "static")

def check_make_directory(directory: str) -> None:
    """
    Checks if a directory doesn't exist, and makes it.
    Attempts to be thread-safe.
    """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            return
        except Exception as ex:
            if not os.path.exists(directory):
                raise IOError(f"Couldn't create directory `{directory}`: {type(ex).__name__}({ex})")
            return

def get_local_configuration(as_api_configuration: bool = False) -> Union[Dict[str, Any], APIConfiguration]:
    """
    Gets configuration from a file in the environment, or the base config.
    """
    default_config = os.path.join(get_local_config_directory(), "server.yml")
    if not os.path.exists(default_config):
        raise IOError(f"Couldn't find or access default configuration at {default_config}")
    user_config = os.getenv("ENFUGUE_CONFIG", None)
    if user_config is not None and not os.path.exists(user_config):
        raise IOError(f"Configuration file {user_config} missing or inaccessible")

    configuration = load_yaml(default_config)
    if "configuration" in configuration:
        configuration = configuration["configuration"]

    if user_config is not None:
        basename, ext = os.path.splitext(os.path.basename(user_config))
        if ext.lower() in [".yml", ".yaml"]:
            user_dict = load_yaml(user_config)
        elif ext.lower() == ".json":
            user_dict = load_json(user_config)
        else:
            raise IOError(f"Unknown extension {ext}")
        if "configuration" in user_dict:
            user_dict = user_dict["configuration"]
        merge_into(user_dict, configuration)

    if as_api_configuration:
        return APIConfiguration(**configuration)
    return configuration

def parse_version(version_string: str) -> Version:
    """
    Parses a version string to a semantic version.
    Does not choke on post-releases, unlike base semver.
    """
    return Version(".".join(version_string.split(".")[:3]))

def get_version() -> Version:
    """
    Gets the version of enfugue installed.
    """
    import logging

    logger = logging.getLogger("enfugue")
    try:
        local_install = get_local_installation_directory()
        version_file = os.path.join(local_install, "version.txt")
        if os.path.exists(version_file):
            with open(version_file, "r") as fp:
                return parse_version(fp.read())
    except:
        pass

    from importlib.metadata import version, PackageNotFoundError

    try:
        return parse_version(version("enfugue"))
    except PackageNotFoundError:
        return Version("0.0.0")


def get_versions() -> List[VersionDict]:
    """
    Gets all version details from the CDN.
    """
    version_data = requests.get("https://cdn.enfugue.ai/versions.json").json()
    versions: List[VersionDict] = [
        cast(
            VersionDict,
            {
                "version": Version(datum["version"]),
                "release": datetime.datetime.strptime(datum["release"], "%Y-%m-%d").date(),
                "description": datum["description"],
            },
        )
        for datum in version_data
    ]
    versions.sort(key=lambda v: v["version"])
    return versions


def get_pending_versions() -> List[VersionDict]:
    """
    Gets only versions yet to be installed.
    """
    current_version = get_version()
    return [version for version in get_versions() if version["version"] > current_version]

def find_file_in_directory(directory: str, file: str, extensions: Optional[List[str]] = None) -> Optional[str]:
    """
    Finds a file in a directory and returns it.
    Uses breadth-first search.
    """
    if not os.path.isdir(directory):
        return None
    if extensions is None:
        file, current_ext = os.path.splitext(file)
        extensions = [current_ext]
    for ext in extensions:
        check_file = os.path.join(directory, f"{file}{ext}")
        if os.path.exists(check_file):
            return check_file
    for filename in os.listdir(directory):
        check_path = os.path.join(directory, filename)
        if os.path.isdir(check_path):
            check_recursed = find_file_in_directory(check_path, file, extensions=extensions)
            if check_recursed is not None:
                return os.path.abspath(check_recursed)
    return None

def find_files_in_directory(directory: str, pattern: Optional[Union[str, re.Pattern]] = None) -> Iterator[str]:
    """
    Find files in a directory, optionally matching a pattern.
    """
    if pattern is not None and isinstance(pattern, str):
        pattern = re.compile(pattern)
    if os.path.isdir(directory):
        for filename in os.listdir(directory):
            check_path = os.path.join(directory, filename)
            if os.path.isdir(check_path):
                for sub_file in find_files_in_directory(check_path, pattern):
                    yield sub_file
            elif pattern is None or bool(pattern.match(filename)):
                yield os.path.abspath(check_path)

def check_make_directory_by_names(root: str, *directory_names: str) -> str:
    """
    Finds a directory from the root, trying many different cases.
    """
    default = os.path.join(root, directory_names[0])
    if os.path.exists(default):
        return default

    from pibble.util.strings import kebab_case, camel_case, pascal_case, snake_case
    all_lowercase = lambda name: re.sub(r"[^a-zA-Z0-9]", "", name).lower()
    all_uppercase = lambda name: re.sub(r"[^a-zA-Z0-9]", "", name).upper()
    all_directory_names = []

    for directory_name in directory_names:
        all_directory_names.append(directory_name)
        if not directory_name.endswith("s"):
            maybe_plural = f"{directory_name}s"
            if maybe_plural not in directory_names:
                all_directory_names.append(maybe_plural)

    for directory_name in all_directory_names:
        default_name = os.path.join(root, directory_name)
        if os.path.exists(default_name):
            return default_name
        for try_method in [snake_case, kebab_case, camel_case, pascal_case, all_lowercase, all_uppercase]:
            maybe = os.path.join(root, try_method(directory_name))
            if os.path.exists(maybe):
                return maybe

    check_make_directory(default)
    return default
