export PYTHONPATH=$(shell pwd)/src/

run:
	@python src/main.py

test:
	@pytest -v

test-matching:
	@pytest -x -s -k $(k) -vvvv

###
# Lint section
###
_ruff:
	@ruff format --check .
	@ruff .

_ruff-fix:
	@ruff format .
	@ruff --fix .

_mypy:
	@mypy src/

pre-commit:
	@pre-commit run --all-files

lint: _ruff _mypy ## Check code lint
format-code: _ruff-fix  ## Format code