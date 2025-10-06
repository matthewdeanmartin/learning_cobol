import logging
import os
import subprocess
from pathlib import Path

import httpx
from httpx import HTTPStatusError
from rich.console import Console

from mainframer.manage_config import DEFAULT_INSTALL_DIR

LOGGER = logging.getLogger(__name__)

# Initialize rich console
console = Console()


# Windows sources. Not nearly enough automation for single click compilation.
# gnucobol-3.1.2_win_src.7z
# gnucobol-3.0-rc1_win.7z
# gnucobol-2.2_win.7z
# gnu-cobol-2.0_rc-2_win.zip
# gnu-cobol-1.1.tar.gz  (src)

windows_binaries = {
    "3.2": "https://www.arnoldtrembley.com/GC32M-BDB-x64.7z",
    "3.1.2": "https://www.arnoldtrembley.com/GC312-BDB-M64-rename-7z-to-exe.7z",
    "3.1-rc1": "https://www.arnoldtrembley.com/GC31-rc1-BDB-M64-rename-7z-to-exe.7z",
    "2.0": "https://www.arnoldtrembley.com/GC20RC2-BDB-rename-7z-to-exe.7z",
    "2.2": "https://www.arnoldtrembley.com/GC22-BDB-rename-7z-to-exe.7z",
    "2.2-b": "https://www.arnoldtrembley.com/GC22B-64bit-rename-7z-to-exe.7z",
    "1.1-open": "https://www.arnoldtrembley.com/OpenCOBOL-MinGw-installer.zip",
    "1.1-gnu": "https://www.arnoldtrembley.com/GnuCOBOL-MinGw-Installer.zip",
}


def get_install_dir() -> Path:
    """Determine the installation directory.

    Returns:
        Path: The path to the installation directory.
    """
    cobol_home = os.getenv("COBOL_HOME")
    if cobol_home:
        return Path(cobol_home)
    return DEFAULT_INSTALL_DIR


def download_file(url: str, dest: Path) -> bool:
    """Download a file from a given URL to a destination.

    Args:
        url (str): The URL to download the file from.
        dest (Path): The destination path to save the file.
    """
    console.print(f"[cyan]Downloading {url} to {dest}...[/cyan]")
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        with open(dest, "wb") as f:
            f.write(response.content)
            # urllib.request.urlretrieve(url, dest)
        return True
    except HTTPStatusError as e:
        console.print(f"[red]Failed to download {url} to {dest}.[/red]")
        console.print(f"[red]{e}[/red]")
        return False


def extract_archive(archive_path: Path, dest_dir: Path) -> None:
    """Extract a .7z archive to a specified directory.

    Args:
        archive_path (Path): The path to the .7z archive.
        dest_dir (Path): The directory to extract the archive into.
    """
    console.print(f"[cyan]Extracting {archive_path} to {dest_dir}...[/cyan]")
    # py7zr doesn't pipx install? maybe it just needs setuptools?
    # with py7zr.SevenZipFile(archive_path, mode='r') as archive:
    #     archive.extractall(path=dest_dir)
    console.print(f"[cyan]Extracting {archive_path} to {dest_dir}...[/cyan]")
    try:
        subprocess.run(["7z", "x", str(archive_path), f"-o{dest_dir}"], check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Failed to extract {archive_path} to {dest_dir}.[/red]")
        console.print(f"[red]{e}[/red]")


def install_cobol_version(command: str, version: str, install_dir: Path | None = None) -> None:
    """Install a specific version of GnuCobol.

    Args:
        command (str): install/build to either install binaries or to download source
        version (str): The version of GnuCobol to install.
        install_dir (Optional[Path]): The directory to install GnuCobol into. Defaults to None.
    """
    if command == "cobc-compile":
        raise NotImplementedError("Source build not implemented yet. Try install")

    if not install_dir:
        install_dir = get_install_dir()

    install_dir.mkdir(parents=True, exist_ok=True)

    archive_name = f"gnucobol-{version}_win.7z"
    _download_url = f"https://sourceforge.net/projects/gnucobol/files/gnucobol/{version}/{archive_name}/download"

    versions = []
    if version == "all":
        versions = list(windows_binaries.keys())
    else:
        versions.append(version)

    for target_version in versions:
        download_one(target_version, install_dir)


def download_one(version: str, install_dir: Path) -> None:
    version_dir = install_dir / f"gnucobol-{version}"
    if version_dir.exists():
        console.print(f"[yellow]GnuCobol version {version} is already installed in {version_dir}.[/yellow]")
        return

    if version not in windows_binaries:
        console.print(f"[red]GnuCobol version {version} is not available for Windows.[/red]")
        console.print("Available versions: ")
        for valid_version in windows_binaries:
            console.print(f"[cyan]     {valid_version}[/cyan]")
        return

    download_url = windows_binaries[version]
    archive_name = download_url.split("/")[-1]
    temp_archive = install_dir / archive_name

    if temp_archive.exists():
        console.print(f"[yellow]GnuCobol version {version} is already downloaded in {temp_archive}.[/yellow]")
        return
    # Download it
    success = download_file(download_url, temp_archive)
    if not success:
        return

    if version_dir.exists() and any(version_dir.iterdir()):
        console.print(f"[yellow]GnuCobol version {version} is already installed in {version_dir}.[/yellow]")
        return

    version_dir.mkdir(parents=True, exist_ok=True)
    extract_archive(temp_archive, version_dir)
    # don't remove file, try to minimize bandwidth costs of host.

    console.print(f"[green]GnuCobol version {version} installed successfully in {version_dir}.[/green]")

    console.print(f"[cyan]Configuration updated with version {version}.[/cyan]")
