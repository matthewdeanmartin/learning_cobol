# if you wrap everything in poetry run, it runs slower.
ifeq ($(origin VIRTUAL_ENV),undefined)
    VENV := poetry run
else
    VENV :=
endif

poetry.lock: pyproject.toml
	@echo "Installing dependencies"
	@poetry install --with dev

clean-pyc:
	@echo "Removing compiled files"
# 	@find mainframer -name '*.pyc' -exec rm -f {} + || true
#	@find mainframer -name '*.pyo' -exec rm -f {} + || true
#	@find mainframer -name '__pycache__' -exec rm -fr {} + || true

clean-test:
	@echo "Removing coverage data"
	@rm -f .coverage || true
	@rm -f .coverage.* || true

clean: clean-pyc clean-test

# tests can't be expected to pass if dependencies aren't installed.
# tests are often slow and linting is fast, so run tests on linted code.
test: clean poetry.lock
	@echo "Running unit tests"
	#  $(VENV) pytest --doctest-modules mainframer
	# $(VENV) python -m unittest discover
	$(VENV) py.test tests -vv -n 2 --cov=mainframer --cov-report=html --cov-fail-under 50
	$(VENV) bash basic_test.sh


.PHONY: isort
isort:
	@echo "Formatting imports"
	$(VENV) isort .

.PHONY: black
black:
	@echo "Formatting code"
	$(VENV) metametameta poetry
	$(VENV) black mainframer --exclude .venv
	$(VENV) black tests --exclude .venv --exclude .tox
	# $(VENV) black scripts --exclude .venv

.PHONY: pre-commit
pre-commit: isort black
	@echo "Pre-commit checks"
	$(VENV) pre-commit run --all-files

.PHONY: bandit
bandit:
	@echo "Security checks"
	$(VENV)  bandit mainframer -r -c pyproject.toml

.PHONY: pylint
pylint: isort black
	@echo "Linting with pylint"
	$(VENV) ruff check --fix
	$(VENV) pylint mainframer --fail-under 9.8

# for when using -j (jobs, run in parallel)
.NOTPARALLEL: isort black

check: mypy test pylint bandit pre-commit

.PHONY: publish
publish: test
	rm -rf dist && poetry build

.PHONY: mypy
mypy:
	$(VENV) mypy mainframer --ignore-missing-imports --check-untyped-defs


check_docs:
	$(VENV) interrogate mainframer --verbose
	$(VENV) pydoctest --config .pydoctest.json | grep -v "__init__" | grep -v "__main__" | grep -v "Unable to parse"

make_docs:
	pdoc mainframer --html -o docs --force

check_md:
	$(VENV) mdformat README.md docs/*.md
	# $(VENV) linkcheckMarkdown README.md # it is attempting to validate ssl certs
	$(VENV) markdownlint README.md --config .markdownlintrc

check_spelling:
	$(VENV) pylint mainframer --enable C0402 --rcfile=.pylintrc_spell
	$(VENV) codespell README.md --ignore-words=private_dictionary.txt
	$(VENV) codespell mainframer --ignore-words=private_dictionary.txt

check_changelog:
	# pipx install keepachangelog-manager
	$(VENV) changelogmanager validate

check_all: check_docs check_md check_spelling check_changelog

