DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1

ASYNCHRONOUS_PATTERN := asynchronous_pattern
ASYNCHRONOUS_PATTERN_PROXY := asynchronous_proxy
ASYNCHRONOUS_PATTERN_PROXY_PORT := 8000
ASYNCHRONOUS_PATTERN_SERVER := imagenet_inception_v3
ASYNCHRONOUS_PATTERN_GRPC_PORT := 8500
ASYNCHRONOUS_PATTERN_REST_PORT := 8501
ASYNCHRONOUS_PATTERN_BACKEND := asynchronous_backend

.PHONY: build_proxy
build_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_PROXY)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).proxy .

.PHONY: push_proxy
push_proxy:
	docker push $(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_PROXY)_$(IMAGE_VERSION)

.PHONY: build_server
build_server:
	docker build \
		-t $(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_SERVER)_$(IMAGE_VERSION) \
		-f ./$(ASYNCHRONOUS_PATTERN_SERVER)/$(DOCKERFILE) .

.PHONY: push_server
push_server:
	docker push $(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_SERVER)_$(IMAGE_VERSION)

.PHONY: build_backend
build_backend:
	docker build \
		-t $(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_BACKEND)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).backend .

.PHONY: run_backend
run_backend:
	docker run \
		-d \
		--name $(ASYNCHRONOUS_PATTERN_BACKEND) \
		$(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_BACKEND)_$(IMAGE_VERSION)

.PHONY: push_backend
push_backend:
	docker push $(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_BACKEND)_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build_proxy build_server build_backend

.PHONY: run_all
run_all: run_proxy run_server run_backend

.PHONY: push_all
push_all: push_proxy push_server push_backend

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
