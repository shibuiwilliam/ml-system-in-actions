DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1

SYNC_ASYNC_PATTERN := sync_async_pattern
SYNC_ASYNC_PATTERN_PROXY := sync_async_proxy
SYNC_ASYNC_PATTERN_PROXY_PORT := 8000
SYNC_ASYNC_PATTERN_SYNC_MODEL := imagenet_mobilenet_v2
SYNC_ASYNC_PATTERN_SYNC_GRPC_PORT := 8500
SYNC_ASYNC_PATTERN_SYNC_REST_PORT := 8501
SYNC_ASYNC_PATTERN_ASYNC_MODEL := imagenet_inception_v3
SYNC_ASYNC_PATTERN_ASYNC_GRPC_PORT := 8600
SYNC_ASYNC_PATTERN_ASYNC_REST_PORT := 8601
SYNC_ASYNC_PATTERN_BACKEND := sync_async_backend

.PHONY: build_proxy
build_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_PROXY)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).proxy .

.PHONY: push_proxy
push_proxy:
	docker push $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_PROXY)_$(IMAGE_VERSION)

.PHONY: build_sync
build_sync:
	docker build \
		-t $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_SYNC_MODEL)_$(IMAGE_VERSION) \
		-f ./$(SYNC_ASYNC_PATTERN_SYNC_MODEL)/$(DOCKERFILE) .

.PHONY: push_sync
push_sync:
	docker push $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_SYNC_MODEL)_$(IMAGE_VERSION)


.PHONY: build_async
build_async:
	docker build \
		-t $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_ASYNC_MODEL)_$(IMAGE_VERSION) \
		-f ./$(SYNC_ASYNC_PATTERN_ASYNC_MODEL)/$(DOCKERFILE) .

.PHONY: push_async
push_async:
	docker push $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_ASYNC_MODEL)_$(IMAGE_VERSION)


.PHONY: build_backend
build_backend:
	docker build \
		-t $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_BACKEND)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).backend .

.PHONY: push_backend
push_backend:
	docker push $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_BACKEND)_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build_proxy build_sync build_async build_backend

.PHONY: push_all
push_all: push_proxy push_sync push_async push_backend

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

