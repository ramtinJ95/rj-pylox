format:
	ruff check --select I --fix
	ruff format
lint:
	ruff check
	mypy .
