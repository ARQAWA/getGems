poetry-lock:
	poetry lock --no-update

poetry-sync:
	poetry install --sync --no-root

poetry-relock: poetry-lock poetry-sync

ruff:
	ruff format --preview && ruff check --preview --fix --unsafe-fixes

include .env
MIGRATIONS_DIR=./migrations

migrate-make:
	@read -p "Enter migration name: " name_; \
	migrate create -ext sql -dir $(MIGRATIONS_DIR) -seq -digits 6 $$name_

migrate-up:
	@echo $(CLICKHOUSE__DSN)
	migrate -database $(CLICKHOUSE__DSN) -path $(MIGRATIONS_DIR) up

migrate-down:
	migrate -database $(CLICKHOUSE__DSN) -path $(MIGRATIONS_DIR) down

migrate-force:
	@read -p "Enter version to force: " vers_; \
	migrate -database $(CLICKHOUSE__DSN) -path $(MIGRATIONS_DIR) force $$vers_