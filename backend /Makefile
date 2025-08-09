# MuseAIka Backend Makefile

.PHONY: help install setup start stop test clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  setup       Setup development environment"
	@echo "  start       Start development server"
	@echo "  stop        Stop all services"
	@echo "  test        Run tests"
	@echo "  clean       Clean generated files"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run  Run with Docker"

install:
	pip install -r requirements.txt

setup:
	python scripts/setup.py

start:
	docker-compose up -d
	python app.py

stop:
	docker-compose down

test:
	python -m pytest tests/ -v --cov=.

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

docker-build:
	docker build -t museaika-backend .

docker-run:
	docker-compose up --build

lint:
	black . --check
	isort . --check-only

format:
	black .
	isort .

security:
	bandit -r . -f json -o security-report.json
