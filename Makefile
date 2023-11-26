clean:
	docker compose down --rmi local -v

stop:
	docker compose down

build: stop
	docker compose build

tests: build
	docker compose up -d
	sleep 5
	docker compose run app bash trigger_tests_on_docker.sh

run:
	docker compose up
