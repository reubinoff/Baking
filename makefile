
DOCKER_REG=reubinoff.azurecr.io/reubinoff

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

deploy:
	cd deployment/charts/baking-server; \
		helm upgrade --install baking-test ./

