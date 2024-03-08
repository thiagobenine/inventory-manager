export PYTHONPATH=$(shell pwd)/src/

run:
	@python src/main.py

test:
	@pytest -v

test-matching:
	@pytest -x -s -k $(k) -vvvv
