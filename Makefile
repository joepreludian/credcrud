clean:
	docker compose down --rmi local -v

stop:
	docker compose down

build: stop
	docker compose build

setup: build
	docker compose up -d
	sleep 5
	docker compose run --rm app alembic upgrade head
	docker compose down

tests: build
	docker compose up -d
	sleep 5
	docker compose run --rm app bash trigger_tests_on_docker.sh

run:
	docker compose up
