DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1


PARAMETER_BASED_PATTERN := parameter_based_pattern
PARAMETER_BASED_PATTERN_PATH := $(ABSOLUTE_PATH)/$(PARAMETER_BASED_PATTERN)
PARAMETER_BASED_PATTERN_SETOSA_PORT := 8000
PARAMETER_BASED_PATTERN_VERSICOLOR_PORT := 8001
PARAMETER_BASED_PATTERN_VIRGINICA_PORT := 8002

PARAMETER_BASED_PATTERN_PROXY_PORT := 9000

.PHONY: build_setosa
build_setosa:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_setosa_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).service.setosa \
		.
	
.PHONY: push_setosa
push_setosa:
	docker push $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_setosa_$(IMAGE_VERSION)


.PHONY: build_versicolor
build_versicolor:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_versicolor_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).service.versicolor \
		.

.PHONY: push_versicolor
push_versicolor:
	docker push $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_versicolor_$(IMAGE_VERSION)


.PHONY: build_virginica
build_virginica:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_virginica_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).service.virginica \
		.
	
.PHONY: push_virginica
push_virginica:
	docker push $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_virginica_$(IMAGE_VERSION)


.PHONY: build_proxy
build_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_proxy_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).proxy \
		.
	
.PHONY: push_proxy
push_proxy:
	docker push $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_proxy_$(IMAGE_VERSION)

.PHONY: build_client
build_client:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_client_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).client \
		.
	
.PHONY: push_client
push_client:
	docker push $(DOCKER_REPOSITORY):$(PARAMETER_BASED_PATTERN)_client_$(IMAGE_VERSION)


.PHONY: build_all
build_all: build_setosa build_versicolor build_virginica build_proxy build_client

.PHONY: push_all
push_all: push_setosa push_versicolor push_virginica push_proxy push_client

.PHONY: c_build
c_build: build_all

.PHONY: c_up
c_up:
	docker-compose \
		-f ./$(DOCKER_COMPOSE) \
		up -d

.PHONY: c_down
c_down:
	docker-compose \
		-f ./$(DOCKER_COMPOSE) \
		down

.PHONY: deploy
deploy:
	kubectl apply -f manifests/namespace.yml
	kubectl apply -f manifests
