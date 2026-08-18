.PHONY: help migrate dev test clean docker-build docker-down

help: ## Show all commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

migrate-up: ## Run Alembic migrations up
	docker compose run --rm dashboardku alembic upgrade head

migrate-down: ## Rollback latest migration
	docker compose run --rm dashboardku alembic downgrade -1

migrate-revision: ## Create new migration file
	docker compose run --rm dashboardku alembic revision --autogenerate -m "$(MESSAGE)"

dev: ## Run development server (localhost)
	python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test: ## Run tests
	python -m pytest tests/ -v

docker-build: ## Build Docker image locally
	docker compose build

docker-up: ## Start containers
	docker compose up

docker-down: ## Stop containers
	docker compose down

docker-ps: ## Show container status
	docker compose ps

log: ## View logs
	docker compose logs -f

shell: ## Enter application shell
	docker compose exec dashboardku bash

mysql-shell: ## Enter MySQL shell
	docker compose exec mysql mysql -u dashboardku -psecret dashboardku
