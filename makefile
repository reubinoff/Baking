
DOCKER_REG=reubinoff.azurecr.io/reubinoff

DB_ROOT_PWD=test
DB_ROOT_USER=root
DB_CONTAINER_NAME=baking_pytest_from_make



build: build-server build-client


test-server:
	cd server; \
		poetry run python -m pytest -xrv --cov=src/baking/routers

run-db:
	docker run --name ${DB_CONTAINER_NAME} --rm -d -e MONGO_INITDB_ROOT_PASSWORD=$(DB_ROOT_PWD) -e MONGO_INITDB_ROOT_USERNAME=$(DB_ROOT_USER) -p 27017:27017 mongo:6.0.5

stop-db:
	$(eval DB_CONTAINER_NAME=$(shell sh -c "docker container ls | grep ${DB_CONTAINER_NAME}" | awk '{print $$1}'))
	@ echo ${DB_CONTAINER_NAME}
	docker stop ${DB_CONTAINER_NAME}

check-updates:
	cd server; \
		poetry run pip list --outdated
	cd react-client; \
		npx npm-check-updates -u
		npm update