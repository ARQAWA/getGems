define check_sha
	([ -f $(1) ] && (shasum $(1) | awk '{ print $$1 }') || echo "") > /tmp/$(1).old_sha
	poetry export --without-hashes -f requirements.txt -o $(1) $(2)
	([ -f $(1) ] && (shasum $(1) | awk '{ print $$1 }') || echo "") > /tmp/.$(1).new_sha
	if diff -q /tmp/$(1).old_sha /tmp/.$(1).new_sha > /dev/null; then \
		echo "$(1) has not changed"; \
		rm /tmp/$(1).old_sha /tmp/.$(1).new_sha; \
	else \
		echo "Error: $(1) has changed!"; \
		rm /tmp/$(1).old_sha /tmp/.$(1).new_sha; \
		exit 1; \
	fi
endef

poetry-lock:
	@poetry lock --no-update

poetry-sync:
	@poetry install --sync --no-root --with dev

poetry-export-reqs:
	@$(call check_sha,requirements.txt,)

sync: poetry-lock poetry-sync poetry-export-reqs

ruff-format:
	@ruff format --preview

ruff-check:
	@ruff check --preview --fix --unsafe-fixes

mypy:
	@mypy app

linters: ruff-format ruff-check mypy

vult:
	@vulture app

include .env
MIGRATIONS_DIR=./migrations

migrate-make:
	@read -p "Enter migration name: " name_; \
	migrate create -ext sql -dir $(MIGRATIONS_DIR) -seq -digits 6 $$name_

migrate-up:
	@echo $(CLICKHOUSE__DSN)
	@migrate -database $(CLICKHOUSE_MIGRATION_DSN) -path $(MIGRATIONS_DIR) up

migrate-down:
	@migrate -database $(CLICKHOUSE_MIGRATION_DSN) -path $(MIGRATIONS_DIR) down

migrate-force:
	@read -p "Enter version to force: " vers_; \
	migrate -database $(CLICKHOUSE_MIGRATION_DSN) -path $(MIGRATIONS_DIR) force $$vers_
