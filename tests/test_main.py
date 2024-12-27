from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mainframer import __main__ as main


@pytest.mark.parametrize(
    "command, args, expected_function, expected_args",
    [
        # Test cobc-install
        (
            ["cobc-install", "3.1.2", "--dir", "/custom/path"],
            {"command": "cobc-install", "version": "3.1.2", "dir": Path("/custom/path")},
            "install_cobol_version",
            ("cobc-install", "3.1.2", Path("/custom/path")),
        ),
        # Test cobc-compile
        (
            ["cobc-compile", "3.1.2", "--dir", "/compile/path"],
            {"command": "cobc-compile", "version": "3.1.2", "dir": Path("/compile/path")},
            "install_cobol_version",
            ("cobc-compile", "3.1.2", Path("/compile/path")),
        ),
        # Test shell
        (
            ["shell"],
            {"command": "shell"},
            "activate_cob_environment",
            (),
        ),
        # Test install
        (
            ["install"],
            {"command": "install"},
            "install_packages",
            (),
        ),
        # Test build
        (
            ["build", "clean"],
            {"command": "build", "subcommand": "clean"},
            "clean",
            (),
        ),
    ],
)
@patch("mainframer.__main__.install_cobol_version")
@patch("mainframer.__main__.activate_cob_environment")
@patch("mainframer.__main__.install_packages")
@patch("mainframer.__main__.COBOLBuilder")
@patch("mainframer.__main__.load_config")
def test_main(
    mock_load_config,
    mock_cobol_builder,
    mock_install_packages,
    mock_activate_cob_environment,
    mock_install_cobol_version,
    command,
    args,
    expected_function,
    expected_args,
):
    """Test the main function with various subcommands."""
    mock_builder_instance = MagicMock()
    mock_cobol_builder.return_value = mock_builder_instance
    mock_load_config.return_value = {"mock": "config"}

    exit_code = main.main(command)

    # Verify exit code
    assert exit_code == 0

    # Verify the correct function is called
    if expected_function == "install_cobol_version":
        mock_install_cobol_version.assert_called_once_with(*expected_args)
    elif expected_function == "activate_cob_environment":
        mock_activate_cob_environment.assert_called_once_with(
            {
                "mock": "config",
            }
        )
    elif expected_function == "install_packages":
        mock_install_packages.assert_called_once_with({"mock": "config"})
    elif expected_function in {"clean", "compile_objects", "build_binary", "run", "test"}:
        getattr(mock_builder_instance, expected_function).assert_called_once_with()

    # Verify global args if present
    if "--verbose" in command:
        assert "verbose" in args


def test_missing_subcommand():
    """Test that missing subcommand raises a SystemExit with usage information."""
    with pytest.raises(SystemExit) as excinfo:
        main.main([])  # No subcommand
    assert excinfo.value.code != 0


def test_help_message(capsys):
    """Test the help message is displayed when requested."""
    with pytest.raises(SystemExit):
        main.main(["--help"])

    captured = capsys.readouterr()
    assert "Manage GnuCobol." in captured.out
    assert "usage:" in captured.out
