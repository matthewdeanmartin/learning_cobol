# Define virtual environment based on whether poetry is used
VENV := poetry run

# Install dependencies
poetry_lock: pyproject.toml
    @echo "Installing dependencies"
    @poetry install --with dev

# Clean .pyc files
clean_pyc:
    @echo "Removing compiled files"
    pyclean

# Clean test data
clean_test:
    @echo "Removing coverage data"
    @rm -f .coverage || true
    @rm -f .coverage.* || true

# Full clean
clean: clean_pyc clean_test

# Run tests with linted code
test: clean poetry_lock
    @echo "Running unit tests"
    $(VENV) py.test tests -vv -n 2 --cov=mainframer --cov-report=html --cov-fail-under 50
    $(VENV) bash basic_test.sh

# Format imports
isort:
    @echo "Formatting imports"
    $(VENV) isort .

# Format code with black
black:
    @echo "Formatting code"
    $(VENV) black mainframer --exclude .venv
    $(VENV) black tests --exclude .venv --exclude .tox

# Run pre-commit checks
pre_commit: isort black
    @echo "Pre-commit checks"
    $(VENV) pre-commit run --all-files

# Security checks with bandit
bandit:
    @echo "Security checks"
    $(VENV) bandit mainframer -r -c pyproject.toml

# Linting with pylint and ruff
pylint: isort black
    @echo "Linting with pylint"
    $(VENV) ruff check --fix
    $(VENV) pylint mainframer --fail-under 9.8

# Run all checks in parallel (except isort and black)
.NOTPARALLEL: isort black

# Full check, including mypy, test, pylint, bandit, and pre-commit
check: mypy test pylint bandit pre_commit

# Publish the project after passing tests
publish: test
    rm -rf dist && poetry build

# Type checking with mypy
mypy:
    $(VENV) mypy mainframer --ignore-missing-imports --check-untyped-defs

# Check documentation
check_docs:
    $(VENV) interrogate mainframer --verbose
    $(VENV) pydoctest --config .pydoctest.json | grep -v "__init__" | grep -v "__main__" | grep -v "Unable to parse"

# Generate HTML documentation with pdoc
make_docs:
    pdoc mainframer --html -o docs --force

# Check Markdown files formatting
check_md:
    $(VENV) mdformat README.md docs/*.md
    $(VENV) markdownlint README.md --config .markdownlintrc

# Check spelling in documentation and code
check_spelling:
    $(VENV) pylint mainframer --enable C0402 --rcfile=.pylintrc_spell
    $(VENV) codespell README.md --ignore-words=private_dictionary.txt
    $(VENV) codespell mainframer --ignore-words=private_dictionary.txt

# Validate changelog
check_changelog:
    $(VENV) changelogmanager validate

# Run all checks
check_all: check_docs check_md check_spelling check_changelog
