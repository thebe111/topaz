.PHONY: tests

run:
	python ./src/main.py

tests:
	pytest --color=yes --showlocals --tb=short -v ./tests

unit-tests:
	pytest --color=yes --showlocals --tb=short -v ./tests/unit

integration-tests:
	pytest --color=yes --showlocals --tb=short -v ./tests/integration
