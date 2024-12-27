from pathlib import Path
from unittest.mock import ANY, MagicMock, patch

import pytest
import shellingham

import mainframer.activate_environment as activate_environment


@pytest.fixture
def config():
    """Provide a sample configuration for the tests."""
    return {
        "project": {
            "gnucobol": "3.1.2",
        }
    }


@pytest.fixture
def mock_install_dir():
    """Mock the DEFAULT_INSTALL_DIR."""
    with patch("mainframer.activate_environment.DEFAULT_INSTALL_DIR", Path("/mock/install/dir")):
        yield


@pytest.fixture
def mock_shellingham():
    """Mock shellingham.detect_shell."""
    with patch("shellingham.detect_shell", return_value=("bash", "/bin/bash")) as mock_shell:
        yield mock_shell


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock()  # Simulate successful execution
        yield mock_run


def test_activate_cob_environment_success(config, mock_install_dir, mock_shellingham, mock_subprocess_run):
    """Test successful activation of the COB environment."""
    mock_environ = {}

    activate_environment.activate_cob_environment(config, mock_environ)

    # Validate the shell detection was called
    mock_shellingham.assert_called_once()

    # Validate the subprocess was called with the correct shell
    mock_subprocess_run.assert_called_once_with(["/bin/bash"], env=ANY, check=True)

    # Validate the environment variables are set
    cob_path = Path("/mock/install/dir/gnucobol-3.1.2").resolve()
    expected_env_vars = {
        "COB": str(cob_path),
        "COB_CFLAGS": f"-I{cob_path / 'include'}",
        "COB_CONFIG_DIR": str(cob_path / "config"),
        "COB_COPY_DIR": str(cob_path / "copy"),
        "COB_LDFLAGS": f"-L{cob_path / 'GnuCOBOL/lib'}",
        "COB_LIBRARY_PATH": str(cob_path / "extras"),
        "PATH": ANY,
    }

    for key, value in expected_env_vars.items():
        assert mock_environ.get(key) == value, mock_environ


def test_activate_cob_environment_shell_detection_failure(config, mock_install_dir):
    """Test activation fails if shell detection fails."""
    with patch(
        "mainframer.activate_environment.shellingham.detect_shell",
        side_effect=shellingham.ShellDetectionFailure("Detection failed"),
    ):
        with pytest.raises(RuntimeError, match="Unable to detect the current shell."):
            activate_environment.activate_cob_environment(config)


def test_activate_cob_environment_shell_launch_failure(config, mock_install_dir, mock_shellingham):
    """Test activation fails if shell launching fails."""
    with patch("subprocess.run", side_effect=FileNotFoundError("Shell not found")):
        with pytest.raises(RuntimeError, match="Unable to launch the shell."):
            activate_environment.activate_cob_environment(config)
