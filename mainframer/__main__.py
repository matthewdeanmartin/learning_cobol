"""
Mainframer is an environment management tool for gnucobol.
"""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from rich.console import Console

from mainframer.__about__ import __version__
from mainframer.activate_environment import activate_cob_environment
from mainframer.build import COBOLBuilder
from mainframer.install_cobols import install_cobol_version
from mainframer.manage_config import load_config
from mainframer.manage_environments import install_packages

console = Console()


def add_global_args(parser: argparse.ArgumentParser) -> None:
    """Add global arguments to the parser.
    Args:
        parser: The parser to add arguments to.
    """
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output.")


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and run the CLI tool.
    Args:
        argv: The arguments to parse.

    Returns:
        int: The exit code.
    """
    parser = argparse.ArgumentParser(description="Manage GnuCobol.")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    cobc_install_parser = subparsers.add_parser("cobc-install", help="Install a specific GnuCobol version.")
    cobc_install_parser.add_argument("version", help="The version of GnuCobol to install.")
    cobc_install_parser.add_argument("--dir", type=Path, help="Specify custom installation directory.")
    add_global_args(cobc_install_parser)

    cobc_compile_parser = subparsers.add_parser("cobc-compile", help="Compile COBC source.")
    cobc_compile_parser.add_argument("version", help="The version of GnuCobol to install.")
    cobc_compile_parser.add_argument("--dir", type=Path, help="Specify custom installation directory.")
    add_global_args(cobc_compile_parser)

    shell_parser = subparsers.add_parser("shell", help="Activate shell.")
    add_global_args(shell_parser)

    install_parser = subparsers.add_parser("install", help="Install packages from mainframer.toml.")
    add_global_args(install_parser)

    build_parser = subparsers.add_parser("build", help="Build project in current directory.")
    build_parser.add_argument(
        "subcommand",
        choices=[
            "clean",
            "compile_objects",
            "build_binary",
            "run",
            "test",
        ],
        help="Command to execute.",
    )
    add_global_args(build_parser)

    args = parser.parse_args(argv)

    config_file = Path("mainframer.toml")
    if args.command == "cobc-install":
        install_cobol_version(args.command, args.version, args.dir)
    elif args.command == "cobc-compile":
        install_cobol_version(args.command, args.version, args.dir)
    elif args.command == "shell":
        config = load_config(config_file)
        activate_cob_environment(config)
    elif args.command == "install":
        config = load_config(config_file)
        install_packages(config)
    elif args.command == "build":
        config = load_config(config_file)
        builder = COBOLBuilder(config)

        if args.subcommand == "clean":
            builder.clean()
        elif args.subcommand == "compile_objects":
            builder.compile_objects()
        elif args.subcommand == "build_binary":
            builder.build_binary()
        elif args.subcommand == "run":
            builder.run()
        elif args.subcommand == "test":
            builder.test()
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main([]))
