import os
from pathlib import Path
from unittest.mock import patch

import pytest

from mainframer.build import COBOLBuilder


@pytest.fixture
def config(tmp_path):
    """Provides a configuration with temporary paths for testing."""
    return {
        "compiler": {
            "compiler": "mock_cobc",
            "src_dir": str(tmp_path / "src"),
            "copybook_dir": "copybooks",
            "objects_dir": str(tmp_path / "out"),
            "main_src": str(tmp_path / "src" / "main.cob"),
            "bin": str(tmp_path / "main_bin"),
            "test_src": [str(tmp_path / "src" / "test1.cob")],
            "test_bin": str(tmp_path / "test_bin"),
        }
    }


@pytest.fixture
def setup_files(config, tmp_path):
    """Creates the directory structure and dummy files."""
    src_dir = tmp_path / "src"
    copybook_dir = src_dir / "copybooks"
    out_dir = tmp_path / "out"

    src_dir.mkdir(parents=True)
    copybook_dir.mkdir(parents=True)
    out_dir.mkdir(parents=True)

    (src_dir / "main.cob").write_text("dummy main COBOL file", encoding="utf-8")
    (src_dir / "test1.cob").write_text("dummy test COBOL file", encoding="utf-8")
    (copybook_dir / "test.cpy").write_text("dummy copybook", encoding="utf-8")


@pytest.fixture
def mock_subprocess_run():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        yield mock_run


def test_cobol_builder_initialization(config, tmp_path):
    builder = COBOLBuilder(config)
    assert builder.cobc == "mock_cobc"
    assert builder.src_dir == Path(config["compiler"]["src_dir"])
    assert builder.cpy_dir == builder.src_dir / "copybooks"
    assert builder.out_dir == Path(config["compiler"]["objects_dir"])
    assert builder.main_src == Path(config["compiler"]["main_src"])
    assert builder.bin == config["compiler"]["bin"]
    # assert builder.test_src == [Path(path) for path in config["compiler"]["test_src"]]
    assert builder.test_bin == config["compiler"]["test_bin"]


def test_clean(config, setup_files, tmp_path):
    builder = COBOLBuilder(config)
    bin_file = Path(config["compiler"]["bin"])
    test_bin_file = Path(config["compiler"]["test_bin"])
    out_dir = Path(config["compiler"]["objects_dir"])

    bin_file.write_text("binary file", encoding="utf-8")
    test_bin_file.write_text("test binary", encoding="utf-8")
    (out_dir / "object.o").write_text("compiled object", encoding="utf-8")

    assert bin_file.exists()
    assert test_bin_file.exists()
    assert out_dir.exists()

    builder.clean()

    assert not bin_file.exists()
    assert not test_bin_file.exists()
    assert not out_dir.exists()


def test_compile_objects(config, setup_files, mock_subprocess_run):
    builder = COBOLBuilder(config)
    builder.compile_objects()

    assert mock_subprocess_run.call_count == len(builder.src)
    for src, obj in zip(builder.src, builder.objects, strict=False):
        mock_subprocess_run.assert_any_call(
            [
                "mock_cobc",
                "-c",
                "-O2",
                "-debug",
                "-Wall",
                "-fnotrunc",
                "-I",
                str(builder.cpy_dir),
                "-o",
                str(obj),
                str(src),
            ],
            cwd=None,
            text=True,
            env=os.environ,
            check=True,
        )
        # These won't exist because we're mocking the subprocess
        # assert obj.exists()


def test_build_binary(config, setup_files, mock_subprocess_run):
    builder = COBOLBuilder(config)
    builder.build_binary()

    mock_subprocess_run.assert_called_once_with(
        [
            "mock_cobc",
            "-x",
            "-O2",
            "-debug",
            "-Wall",
            "-fnotrunc",
            "-I",
            str(builder.cpy_dir),
            "-o",
            builder.bin,
            str(builder.main_src),
            *map(str, builder.objects),
        ],
        cwd=None,
        text=True,
        env=os.environ,
        check=True,
    )


def test_run(config, setup_files, mock_subprocess_run):
    builder = COBOLBuilder(config)
    builder.run()

    mock_subprocess_run.assert_called_once_with(
        [f"./{builder.bin}"],
        cwd=None,
        text=True,
        env=os.environ,
        check=True,
    )


def test_test(config, setup_files, mock_subprocess_run):
    builder = COBOLBuilder(config)
    builder.test()

    mock_subprocess_run.assert_any_call(
        [
            "mock_cobc",
            "-x",
            "-debug",
            "-Wall",
            "-fnotrunc",
            "-lstdc++",
            "-I",
            str(builder.cpy_dir),
            "-o",
            builder.test_bin,
            *map(str, builder.test_src),
            *map(str, builder.src),
        ],
        cwd=None,
        text=True,
        env=os.environ,
        check=True,
    )

    mock_subprocess_run.assert_any_call(
        ["COB_PRE_LOAD=.venv", f"./{builder.test_bin}"],
        cwd=None,
        text=True,
        env=os.environ,
        check=True,
    )
