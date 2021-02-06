DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1

BATCH_PATTERN := batch_pattern
BATCH_PATTERN_PORT := 8000


.PHONY: build_api
build_api:
	docker build \
		-t $(DOCKER_REPOSITORY):$(BATCH_PATTERN)_api_$(IMAGE_VERSION) \
		-f $(DOCKERFILE).api \
		.
	 
.PHONY: stop_api
stop_api:
	docker rm -f $(BATCH_PATTERN)_api

.PHONY: push_api
push_api:
	docker push $(DOCKER_REPOSITORY):$(BATCH_PATTERN)_api_$(IMAGE_VERSION)

.PHONY: build_batch
build_batch:
	docker build \
		-t $(DOCKER_REPOSITORY):$(BATCH_PATTERN)_batch_$(IMAGE_VERSION) \
		-f $(DOCKERFILE).batch \
		.
	 
.PHONY: stop_batch
stop_batch:
	docker rm -f $(BATCH_PATTERN)_batch

.PHONY: push_batch
push_batch:
	docker push $(DOCKER_REPOSITORY):$(BATCH_PATTERN)_batch_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build_api build_batch


.PHONY: push_all
push_all: push_api push_batch

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
	kubectl apply -f manifests/


