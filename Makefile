.PHONY: install run test lint format up down

install:
	python -m pip install -U pip
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest --junitxml=pytest-report.xml

lint:
	ruff check .

format:
	ruff format .

up:
	docker-compose up --build

down:
	docker-compose down
