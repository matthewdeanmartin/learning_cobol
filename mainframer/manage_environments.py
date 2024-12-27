import logging
import os
import zipfile
from pathlib import Path
from typing import Any

import requests

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def create_venv_folder(venv_path: Path = Path(".venv")):
    """Creates a .venv folder if it doesn't exist."""
    venv_path.mkdir(exist_ok=True)
    LOGGER.info("Created .venv folder at %s", venv_path)
    # write a .gitignore file to the .venv folder
    with (venv_path / ".gitignore").open("w", encoding="utf-8") as file:
        file.write("*\n")


def download_and_process_package(venv_folder: Path, name: str, version: str, url: str):
    """Downloads and processes the package from the given repository URL."""
    package_folder = venv_folder / name
    package_folder.mkdir(exist_ok=True)

    # Construct URL and download the package
    os_name = os.name  # 'posix' for Unix-like, 'nt' for Windows
    zip_filename = f"{name}_{version}_{os_name}.zip"
    zip_url = f"https://{url}/dist/{zip_filename}"
    zip_path = package_folder / zip_filename

    LOGGER.info("Downloading %s...", zip_url)
    response = requests.get(zip_url, stream=True, timeout=10)
    response.raise_for_status()

    with zip_path.open("wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    LOGGER.info("Downloaded %s", zip_filename)

    # Unzip the file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(package_folder)
    LOGGER.info("Extracted %s to %s", zip_filename, package_folder)

    # Move .dll or .so files to .venv
    for dll_file in package_folder.glob("**/*"):
        if dll_file.suffix in (".dll", ".so"):
            destination = Path(".venv") / dll_file.name
            dll_file.rename(destination)
            LOGGER.info("Moved %s to %s", dll_file, destination)

    # Clean up zip file
    zip_path.unlink()


def install_packages(
    config: dict[str, Any], venv_folder: Path = Path(".venv"), gitignore_path: Path = Path(".gitignore")
):
    """Install packages listed in the given TOML file."""
    packages = config.get("packages", {})
    if not packages:
        LOGGER.error("No packages found in to install")
        return

    # Execute steps
    create_venv_folder(venv_folder)
    for name, details in packages.items():
        version = details.get("version")
        url = details.get("url")
        if not version or not url:
            LOGGER.warning("Skipping package %s due to missing version or url", name)
            continue

        download_and_process_package(venv_folder, name, version, url)
