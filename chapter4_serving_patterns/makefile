DOCKER_REPOSITORY := shibui/ml-system-in-action

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := dockercompose.yaml
IMAGE_VERSION := 0.0.1

WEB_SERVING_PATTERN := web_single_pattern
WEB_SERVING_PATTERN_PATH := $(ABSOLUTE_PATH)/$(WEB_SERVING_PATTERN)
WEB_SERVING_PATTERN_PORT := 8000


.PHONY: build_web_serving_pattern
build_web_serving_pattern:
	docker build \
		-t $(DOCKER_REPOSITORY):$(WEB_SERVING_PATTERN)_$(IMAGE_VERSION) \
		-f $(WEB_SERVING_PATTERN_PATH)/$(DOCKERFILE) \
		.
	
.PHONY: run_web_serving_pattern
run_web_serving_pattern:
	docker run \
		-d \
		--name $(WEB_SERVING_PATTERN) \
		-p $(WEB_SERVING_PATTERN_PORT):$(WEB_SERVING_PATTERN_PORT) \
		$(DOCKER_REPOSITORY):$(WEB_SERVING_PATTERN)_$(IMAGE_VERSION)

.PHONY: stop_web_serving_pattern
stop_web_serving_pattern:
	docker rm -f $(WEB_SERVING_PATTERN)

.PHONY: push_web_serving_pattern
push_web_serving_pattern:
	docker push $(DOCKER_REPOSITORY):$(WEB_SERVING_PATTERN)_$(IMAGE_VERSION)


SYNCHRONOUS_PATTERN := synchronous_pattern
SYNCHRONOUS_PATTERN_SERVER := imagenet_inception_v3
SYNCHRONOUS_PATTERN_GRPC_PORT := 8500
SYNCHRONOUS_PATTERN_REST_PORT := 8501


.PHONY: build_synchronous_pattern_server
build_synchronous_pattern_server:
	docker build \
		-t $(DOCKER_REPOSITORY):$(SYNCHRONOUS_PATTERN)_$(SYNCHRONOUS_PATTERN_SERVER)_$(IMAGE_VERSION) \
		-f $(SYNCHRONOUS_PATTERN)/$(SYNCHRONOUS_PATTERN_SERVER)/$(DOCKERFILE) .

.PHONY: run_synchronous_pattern_server
run_synchronous_pattern_server:
	docker run \
		-d \
		--name $(SYNCHRONOUS_PATTERN_SERVER) \
		-p $(SYNCHRONOUS_PATTERN_GRPC_PORT):$(SYNCHRONOUS_PATTERN_GRPC_PORT) \
		-p $(SYNCHRONOUS_PATTERN_REST_PORT):$(SYNCHRONOUS_PATTERN_REST_PORT) \
		$(DOCKER_REPOSITORY):$(SYNCHRONOUS_PATTERN)_$(SYNCHRONOUS_PATTERN_SERVER)_$(IMAGE_VERSION)

ASYNCHRONOUS_PATTERN := asynchronous_pattern
ASYNCHRONOUS_PATTERN_PROXY := asynchronous_proxy
ASYNCHRONOUS_PATTERN_PROXY_PORT := 8000
ASYNCHRONOUS_PATTERN_SERVER := imagenet_inception_v3
ASYNCHRONOUS_PATTERN_GRPC_PORT := 8500
ASYNCHRONOUS_PATTERN_REST_PORT := 8501
ASYNCHRONOUS_PATTERN_BACKEND := asynchronous_backend

.PHONY: build_asynchronous_pattern_proxy
build_asynchronous_pattern_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_PROXY)_$(IMAGE_VERSION) \
		-f $(ASYNCHRONOUS_PATTERN)/$(DOCKERFILE).proxy .

.PHONY: run_asynchronous_pattern_proxy
run_asynchronous_pattern_proxy:
	docker run \
		-d \
		--name $(ASYNCHRONOUS_PATTERN_PROXY) \
		-p $(ASYNCHRONOUS_PATTERN_PROXY_PORT):$(ASYNCHRONOUS_PATTERN_PROXY_PORT) \
		$(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_PROXY)_$(IMAGE_VERSION)

.PHONY: build_asynchronous_pattern_server
build_asynchronous_pattern_server:
	docker build \
		-t $(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_SERVER)_$(IMAGE_VERSION) \
		-f $(ASYNCHRONOUS_PATTERN)/$(ASYNCHRONOUS_PATTERN_SERVER)/$(DOCKERFILE) .

.PHONY: run_asynchronous_pattern_server
run_asynchronous_pattern_server:
	docker run \
		-d \
		--name $(ASYNCHRONOUS_PATTERN_SERVER) \
		-p $(ASYNCHRONOUS_PATTERN_GRPC_PORT):$(ASYNCHRONOUS_PATTERN_GRPC_PORT) \
		-p $(ASYNCHRONOUS_PATTERN_REST_PORT):$(ASYNCHRONOUS_PATTERN_REST_PORT) \
		$(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_SERVER)_$(IMAGE_VERSION)

.PHONY: build_asynchronous_pattern_backend
build_asynchronous_pattern_backend:
	docker build \
		-t $(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_BACKEND)_$(IMAGE_VERSION) \
		-f $(ASYNCHRONOUS_PATTERN)/$(DOCKERFILE).backend .

.PHONY: run_asynchronous_pattern_backend
run_asynchronous_pattern_backend:
	docker run \
		-d \
		--name $(ASYNCHRONOUS_PATTERN_PROXY) \
		$(DOCKER_REPOSITORY):$(ASYNCHRONOUS_PATTERN)_$(ASYNCHRONOUS_PATTERN_BACKEND)_$(IMAGE_VERSION)

.PHONY: build_asynchronous_pattern
build_asynchronous_pattern:
	docker-compose \
		-f $(ASYNCHRONOUS_PATTERN)/$(DOCKER_COMPOSE) \
		build

.PHONY: up_asynchronous_pattern
up_asynchronous_pattern:
	docker-compose \
		-f $(ASYNCHRONOUS_PATTERN)/$(DOCKER_COMPOSE) \
		up -d

.PHONY: down_asynchronous_pattern
down_asynchronous_pattern:
	docker-compose \
		-f $(ASYNCHRONOUS_PATTERN)/$(DOCKER_COMPOSE) \
		down


PREP_PRED_PATTERN := prep_pred_pattern
PREP_PRED_PATTERN_PREP := prep
PREP_PRED_PATTERN_PREP_PORT := 8000
PREP_PRED_PATTERN_PRED := pred
PREP_PRED_PATTERN_REST_PORT := 8001
PREP_PRED_PATTERN_GRPC_PORT := 50051

.PHONY: build_prep_pred_pattern_prep
build_prep_pred_pattern_prep:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(PREP_PRED_PATTERN_PREP)_$(IMAGE_VERSION) \
		-f $(PREP_PRED_PATTERN)/$(DOCKERFILE).prep .

.PHONY: run_prep_pred_pattern_prep
run_prep_pred_pattern_prep:
	docker run \
		-d \
		--name $(PREP_PRED_PATTERN_PREP) \
		-p $(PREP_PRED_PATTERN_PREP_PORT):$(PREP_PRED_PATTERN_PREP_PORT) \
		$(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(PREP_PRED_PATTERN_PREP)_$(IMAGE_VERSION)

.PHONY: build_prep_pred_pattern_pred
build_prep_pred_pattern_pred:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(PREP_PRED_PATTERN_PRED)_$(IMAGE_VERSION) \
		-f $(PREP_PRED_PATTERN)/$(DOCKERFILE).pred .

.PHONY: run_prep_pred_pattern_pred
run_prep_pred_pattern_pred:
	docker run \
		-d \
		--name $(PREP_PRED_PATTERN_PRED) \
		-p $(PREP_PRED_PATTERN_GRPC_PORT):$(PREP_PRED_PATTERN_GRPC_PORT) \
		-p $(PREP_PRED_PATTERN_REST_PORT):$(PREP_PRED_PATTERN_REST_PORT) \
		$(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(PREP_PRED_PATTERN_PRED)_$(IMAGE_VERSION)


.PHONY: build_prep_pred_pattern
build_prep_pred_pattern:
	docker-compose \
		-f $(PREP_PRED_PATTERN)/$(DOCKER_COMPOSE) \
		build

.PHONY: up_prep_pred_pattern
up_prep_pred_pattern:
	docker-compose \
		-f $(PREP_PRED_PATTERN)/$(DOCKER_COMPOSE) \
		up -d

.PHONY: down_prep_pred_pattern
down_prep_pred_pattern:
	docker-compose \
		-f $(PREP_PRED_PATTERN)/$(DOCKER_COMPOSE) \
		down