.PHONY: help dev migrate-up migrate-down migrate-revision mysql-up mysql-down mysql-ps mysql-shell mysql-logs

help: ## Show all commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-18s %s\n", $$1, $$2}'

dev: ## Run Flask development server (venv, port 5000)
	.venv/bin/flask run --host 0.0.0.0 --port 5000 --debug

migrate-up: ## Run Alembic migrations up (local venv)
	.venv/bin/alembic upgrade head

migrate-down: ## Rollback latest migration
	.venv/bin/alembic downgrade -1

migrate-revision: ## Create new migration file (MESSAGE="...")
	.venv/bin/alembic revision --autogenerate -m "$(MESSAGE)"

mysql-up: ## Start MySQL container (Docker hanya untuk MySQL di fase ini)
	docker compose up -d mysql

mysql-down: ## Stop MySQL container
	docker compose stop mysql

mysql-ps: ## Show MySQL container status
	docker compose ps

mysql-shell: ## Enter MySQL shell
	docker compose exec mysql mysql -u dashboardku -psecret dashboardku

mysql-logs: ## View MySQL logs
	docker compose logs -f mysql
