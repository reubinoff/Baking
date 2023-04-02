
DOCKER_REG=reubinoff.azurecr.io/reubinoff

DB_ROOT_PWD=rootsql

DB_CONTAINER_NAME=baking_pytest_from_make

build-server:
	cd server; \
		docker-compose build
	docker tag reubinoff/baking:latest $(DOCKER_REG)/baking:latest
	minikube image load $(DOCKER_REG)/baking:latest

build-client:
	cd flutter_client; \
		~/development/flutter/bin/flutter build web
	cp -rf flutter_client/build/web/ web-server/public/
	cd web-server; \
		docker-compose build
	docker tag reubinoff/web:latest $(DOCKER_REG)/web:latest
	minikube image load $(DOCKER_REG)/web:latest


build: build-server build-client


test-server:
	cd server; \
		poetry run python -m pytest -xv

run-db:
	docker run --name ${DB_CONTAINER_NAME} --rm -d -e POSTGRES_PASSWORD=$(DB_ROOT_PWD) -p 5432:5432 postgres:14.6-alpine 

stop-db:
	$(eval DB_CONTAINER_NAME=$(shell sh -c "docker container ls | grep ${DB_CONTAINER_NAME}" | awk '{print $$1}'))
	@ echo ${DB_CONTAINER_NAME}
	docker stop ${DB_CONTAINER_NAME}
