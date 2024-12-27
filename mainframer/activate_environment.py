import logging
import os
import subprocess
from typing import Any

import shellingham
from rich.console import Console

from mainframer.manage_config import DEFAULT_INSTALL_DIR

LOGGER = logging.getLogger(__name__)

# Initialize rich console
console = Console()


def activate_cob_environment(config: dict[str, Any], environ=None) -> dict[str, str]:
    """
    Activates a COB environment by setting necessary environment variables and starting a subshell.

    This function exports specific environment variables required for COBOL tools and opens
    a subshell with those variables set. It uses the `shellingham` library to detect the user's
    current shell and launches it with the modified environment.

    Raises:
        RuntimeError: If the user's shell cannot be detected or if launching the shell fails.
    """
    if environ is None:
        environ = os.environ
    # Get the gnucobol key of [project]
    version = config.get("project", {}).get("gnucobol")
    path_to_cobc = DEFAULT_INSTALL_DIR / f"gnucobol-{version}"

    cob_path = path_to_cobc.resolve()
    environment = {
        "COB": str(cob_path),
        "COB_CFLAGS": f"-I{cob_path / 'include'}",
        "COB_CONFIG_DIR": str(cob_path / "config"),
        "COB_COPY_DIR": str(cob_path / "copy"),
        "COB_LDFLAGS": f"-L{cob_path / 'GnuCOBOL/lib'}",
        "COB_LIBRARY_PATH": str(cob_path / "extras"),
        "PATH": f"{cob_path / 'bin'}{os.pathsep}{os.environ.get('PATH', '')}",
    }

    LOGGER.info("Setting COB environment variables.")
    for key, value in environment.items():
        environ[key] = value
        LOGGER.debug("Set %s=%s", key, value)

    # Detect the user's current shell
    try:
        shell_name, shell_path = shellingham.detect_shell()
        LOGGER.info("Detected shell: %s (%s)", shell_name, shell_path)
    except shellingham.ShellDetectionFailure as error:
        LOGGER.error("Failed to detect shell: %s", error)
        raise RuntimeError("Unable to detect the current shell.") from error

    # Launch the detected shell in interactive mode
    try:
        console.print(f"Launching the shell with for gnucobol-{version} at {cob_path}.")
        subprocess.run([shell_path], env=environ, check=True)
    except FileNotFoundError as error:
        LOGGER.error("Failed to launch the shell: %s", error)
        raise RuntimeError("Unable to launch the shell.") from error
    # return for unit testing.
    return environment
