include .env

DOCKER_EXEC = docker exec app
ALEMBIC_CMD = $(DOCKER_EXEC) alembic -c db/alembic.ini

.PHONY: new_migration
new_migration:
	$(ALEMBIC_CMD) --name=main_db revision --autogenerate -m "$(name)"

.PHONY: upgrade
upgrade:
	$(ALEMBIC_CMD) --name=main_db upgrade head

.PHONY: downgrade
downgrade:
	$(ALEMBIC_CMD) --name=main_db downgrade -1

.PHONY: downgrade_to
downgrade_to:
	$(ALEMBIC_CMD) --name=main_db downgrade "$(name)"

.PHONY: upgrade_test
upgrade_test:
	$(ALEMBIC_CMD) --name=test_db upgrade head

.PHONY: downgrade_test
downgrade_test:
	$(ALEMBIC_CMD) --name=test_db downgrade -1

.PHONY: downgrade_test_to
downgrade_test_to:
	$(ALEMBIC_CMD) --name=test_db downgrade "$(name)"

.PHONY: upgrade_all
upgrade_all: upgrade upgrade_test

.PHONY: downgrade_all
downgrade_all: downgrade downgrade_test

.PHONY: downgrade_to_all
downgrade_to_all: downgrade_to downgrade_test_to

.PHONY: history
history:
	$(ALEMBIC_CMD) history

.PHONY: create_admin
create_admin:
	$(DOCKER_EXEC) python db/default_data_init.py

.PHONY: all
all: upgrade create_admin
