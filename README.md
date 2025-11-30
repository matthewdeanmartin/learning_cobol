# Learning Cobol

## Archived.

See matthewdeanmartin/mainframer for the continuation

## Goals

This is me doing some recreational programming with GnuCOBOL

## Quick Start


```shell
# Install mainframer
poetry install
poetry shell
# Works for windows today, gets and unzips to ~/.cobols/
mainframer install 3.2
# This repo is a monorepo
cd projects/data_structures
# Activate a cobol virtual environment (sets environment variables and path)
mainframer shell
mainframer build build_binary
mainframer build run
```
Wait, surprise gnucobol 3.2 is bundled with Python 3.10.12. After you activate 3.2, python is now 3.10.12!

You can also do the above with the `cobenv.sh` and `Makefile`.


## Opinions

- COBOL is a low level language.
- It is like a DSL for file-based ETL.
- It is very fast
- It has C interop

But
- The first pain point is code reuse patterns, e.g. function and class analogues.
- The other pain point is data structures, e.g. lists, dicts, sets, etc
- The other pain point is package support

Probably no new COBOL code is being written anymore outside of emergency changes to old
code that organizations can't migrate. `mainframer` solves none of those problems. The goal
is to make COBOL development for new projects more modern.

## Experiments so far

- Print and Input - "Text book" COBOL with only Screen, Memory and Keyboard. This sort of code has the fewest 
  problems with COBOL dialect
- Subprocesses - Interop on the shell level.
- Modules - CALL-able code
- Functions - More restricted than CALL-able code
- Includes - Copybooks

## TODO
- Build script
- Package manager
- Multi-gnucobol installer
- Virtual environments

## Windows Installation
- [Source](https://sourceforge.net/projects/gnucobol/files/gnucobol/) Windows build is difficult.
- [Chocolatey](https://community.chocolatey.org/packages/gnucobol)
- [Arnold Trembley](https://www.arnoldtrembley.com) Precompiled binaries for Windows

## Tutorials
- [COBOL Tutorial](https://www.mainframestechhelp.com/tutorials/cobol/basic-verbs.htm)

## Online Tools
- [Online Compiler](https://www.jdoodle.com/execute-cobol-online)

## Example Code
- [CobolCraft, an Example Modern App](https://github.com/meyfa/CobolCraft)

## IDE
- [OpenCobolIDE](https://pypi.org/project/OpenCobolIDE/) This fails to install with pipx for me on windows.
- VSCode has a COBOL plugin
- Jetbrains products do not have a COBOL plugin of any sort, AFAIK.