COMPOSE_FILE := docker/docker-compose.yml
DC := docker-compose -f $(COMPOSE_FILE)

.PHONY: server clean build restart logs test

server:
	$(DC) up -d

clean:
	$(DC) down

build:
	$(DC) build

restart: clean server

logs:
	$(DC) logs -f

test:
	$(DC) run --rm -e POETRY_VIRTUALENVS_IN_PROJECT=false app bash -c "cd /app/backend && poetry lock && poetry install --with test && PYTHONPATH=/app/backend poetry run pytest tests/ -v"
