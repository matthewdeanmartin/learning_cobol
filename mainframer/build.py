import logging
import os
import subprocess
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


class COBOLBuilder:
    def __init__(self, config: dict[str, Any]):
        self.config = config

        compiler = self.config.get("compiler", {})
        self.cobc = compiler.get("compiler", "cobc")
        self.src_dir = Path(compiler.get("src_dir", "src"))
        self.cpy_dir = self.src_dir / compiler.get("copybook_dir", "copybooks")
        self.out_dir = Path(compiler.get("objects_dir", "out"))
        self.main_src = Path(compiler.get("main_src", "main.cob"))
        self.bin = compiler.get("bin", "main")
        self.test_src = [Path("test.cob")] + [Path(p) for p in compiler.get("test_src", "tests")]
        self.test_bin = compiler.get("test_bin", "test")

        self.src = list(self.src_dir.glob("**/*.cob"))
        self.cpy = list(self.cpy_dir.glob("*.cpy"))
        self.objects = [self.out_dir / src.relative_to(self.src_dir).with_suffix(".o") for src in self.src]

    def run_command(self, command: list[str], cwd: Path | None = None):
        """Run a shell command and raise an exception if it fails."""
        LOGGER.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, cwd=cwd, text=True, env=os.environ, check=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {' '.join(command)}")

    def clean(self):
        """Clean the build artifacts."""
        for path in [self.out_dir, Path(self.bin), Path(self.test_bin)]:
            if path.is_dir():
                for item in path.iterdir():
                    item.unlink()
                path.rmdir()
            elif path.is_file():
                path.unlink()

    def compile_objects(self):
        """Compile COBOL source files into objects."""
        for src, obj in zip(self.src, self.objects, strict=False):
            obj.parent.mkdir(parents=True, exist_ok=True)
            self.run_command(
                [
                    self.cobc,
                    "-c",
                    "-O2",
                    "-debug",
                    "-Wall",
                    "-fnotrunc",
                    "-I",
                    str(self.cpy_dir),
                    "-o",
                    str(obj),
                    str(src),
                ]
            )

    def build_binary(self):
        """Build the main binary."""
        self.run_command(
            [
                self.cobc,
                "-x",
                "-O2",
                "-debug",
                "-Wall",
                "-fnotrunc",
                "-I",
                str(self.cpy_dir),
                "-o",
                self.bin,
                str(self.main_src),
                *map(str, self.objects),
            ]
        )

    def run(self):
        """Run the main binary."""
        self.run_command([f"./{self.bin}"])

    def test(self):
        """Build and run tests."""
        self.run_command(
            [
                self.cobc,
                "-x",
                "-debug",
                "-Wall",
                "-fnotrunc",
                "-lstdc++",
                "-I",
                str(self.cpy_dir),
                "-o",
                self.test_bin,
                *map(str, self.test_src),
                *map(str, self.src),
            ]
        )
        self.run_command(["COB_PRE_LOAD=.venv", f"./{self.test_bin}"])
