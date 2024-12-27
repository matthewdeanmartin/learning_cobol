# metametameta

Package manager for gnuCOBOL. Very alpha right now. Not all commands work.

## Installation

```bash
pipx install mainframer
```

## Usage

Installs various versions of gnuCOBOL to `~/.cobol/`
```bash
mainframer cobol 3.2
mainframer cobol 3.2.2
mainframer cobol 3.2-b
```

Now create a `mainframer.toml` in your project root. This is a monorepo, so you can have multiple `mainframer.toml` 
files with at minimum the gnucobol version.

```toml
[project]
gnucobol = "3.2"

[compiler]
# modify compiler options here.

[packages]
"name" = { version="1.2.3", url="github.com/matthewdeanmartin/mainframer" }
```

Activate a cobol. This adds the necessary environment variables.
```bash
mainframer shell
```

Build a cobol project, assuming a particular layout.
```bash
mainframer build compile_objects
mainframer build build_binary
mainframer build test
mainframer build run
```

Help for CLI
```text
usage: mainframer [-h] [-V] {cobol,shell,install,build,clean,test,run} ...
Manage GnuCobol.
positional arguments:
options:
  -h, --help            show this help message and exit
  -V, --version         Show program's version number and exit.
```

## Motivation and Goals

Trying to make a package manager for COBOL.

## Prior Art
- Build script inspired by [CobolCraft](https://github.com/meyfa/CobolCraft)
