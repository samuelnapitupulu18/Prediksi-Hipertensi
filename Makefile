.PHONY: up down build migrate seed fresh logs logs-ml test-be test-fe test-ml shell-be shell-ml health

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up --build -d

migrate:
	docker compose exec backend php artisan migrate

seed:
	docker compose exec backend php artisan db:seed

fresh:
	docker compose exec backend php artisan migrate:fresh --seed

logs:
	docker compose logs -f

logs-ml:
	docker compose logs -f ml-engine

test-be:
	docker compose exec backend php artisan test

test-fe:
	docker compose exec frontend npm run test

test-ml:
	docker compose exec ml-engine pytest

shell-be:
	docker compose exec backend bash

shell-ml:
	docker compose exec ml-engine bash

health:
	docker compose ps
