install:
	poetry install

update:
	poetry update

run_server:
	python main.py

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=src --cov-config=.coveragerc --cov-report  xml

lint:
	poetry run flake8