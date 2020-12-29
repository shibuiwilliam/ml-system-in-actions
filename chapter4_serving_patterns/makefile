DOCKER_REPOSITORY := shibui/ml-system-in-action

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := dockercompose.yaml
IMAGE_VERSION := 0.0.1

WEB_SINGLE_PATTERN := web_single_pattern
WEB_SINGLE_PATTERN_PATH := $(ABSOLUTE_PATH)/$(WEB_SINGLE_PATTERN)
WEB_SINGLE_PATTERN_PORT := 8000


.PHONY: build_web_single_pattern
build_web_single_pattern:
	docker build \
		-t $(DOCKER_REPOSITORY):$(WEB_SINGLE_PATTERN)_$(IMAGE_VERSION) \
		-f $(WEB_SINGLE_PATTERN_PATH)/$(DOCKERFILE) \
		.
	 
.PHONY: run_web_single_pattern
run_web_single_pattern:
	docker run \
		-d \
		--name $(WEB_SINGLE_PATTERN) \
		-p $(WEB_SINGLE_PATTERN_PORT):$(WEB_SINGLE_PATTERN_PORT) \
		$(DOCKER_REPOSITORY):$(WEB_SINGLE_PATTERN)_$(IMAGE_VERSION)

.PHONY: stop_web_single_pattern
stop_web_single_pattern:
	docker rm -f $(WEB_SINGLE_PATTERN)

.PHONY: push_web_single_pattern
push_web_single_pattern:
	docker push $(DOCKER_REPOSITORY):$(WEB_SINGLE_PATTERN)_$(IMAGE_VERSION)


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
		--name $(ASYNCHRONOUS_PATTERN_BACKEND) \
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

HORIZONTAL_MICROSERVICE_PATTERN := horizontal_microservice_pattern
HORIZONTAL_MICROSERVICE_PATTERN_PATH := $(ABSOLUTE_PATH)/$(HORIZONTAL_MICROSERVICE_PATTERN)
HORIZONTAL_MICROSERVICE_PATTERN_SETOSA_PORT := 8000
HORIZONTAL_MICROSERVICE_PATTERN_VERSICOLOR_PORT := 8001
HORIZONTAL_MICROSERVICE_PATTERN_VIRGINICA_PORT := 8002

HORIZONTAL_MICROSERVICE_PATTERN_PROXY_PORT := 9000

.PHONY: build_horizontal_microservice_pattern_setosa
build_horizontal_microservice_pattern_setosa:
	docker build \
		-t $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_setosa_$(IMAGE_VERSION) \
		-f $(HORIZONTAL_MICROSERVICE_PATTERN_PATH)/$(DOCKERFILE).service.setosa \
		.
	
.PHONY: run_horizontal_microservice_pattern_setosa
run_horizontal_microservice_pattern_setosa:
	docker run \
		-d \
		--name $(HORIZONTAL_MICROSERVICE_PATTERN)_setosa \
		-e MODE:setosa \
		-e PORT:$(HORIZONTAL_MICROSERVICE_PATTERN_SETOSA_PORT) \
		-p $(HORIZONTAL_MICROSERVICE_PATTERN_SETOSA_PORT):$(HORIZONTAL_MICROSERVICE_PATTERN_SETOSA_PORT) \
		$(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_setosa_$(IMAGE_VERSION)

.PHONY: stop_horizontal_microservice_pattern_setosa
stop_horizontal_microservice_pattern_setosa:
	docker rm -f $(HORIZONTAL_MICROSERVICE_PATTERN)_setosa


.PHONY: build_horizontal_microservice_pattern_versicolor
build_horizontal_microservice_pattern_versicolor:
	docker build \
		-t $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_versicolor_$(IMAGE_VERSION) \
		-f $(HORIZONTAL_MICROSERVICE_PATTERN_PATH)/$(DOCKERFILE).service.versicolor \
		.
	
.PHONY: run_horizontal_microservice_pattern_versicolor
run_horizontal_microservice_pattern_versicolor:
	docker run \
		-d \
		--name $(HORIZONTAL_MICROSERVICE_PATTERN)_versicolor \
		-e MODE:versicolor \
		-e PORT:$(HORIZONTAL_MICROSERVICE_PATTERN_VERSICOLOR_PORT) \
		-p $(HORIZONTAL_MICROSERVICE_PATTERN_VERSICOLOR_PORT):$(HORIZONTAL_MICROSERVICE_PATTERN_VERSICOLOR_PORT) \
		$(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_versicolor_$(IMAGE_VERSION)

.PHONY: stop_horizontal_microservice_pattern_versicolor
stop_horizontal_microservice_pattern_versicolor:
	docker rm -f $(HORIZONTAL_MICROSERVICE_PATTERN)_versicolor

.PHONY: build_horizontal_microservice_pattern_virginica
build_horizontal_microservice_pattern_virginica:
	docker build \
		-t $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_virginica_$(IMAGE_VERSION) \
		-f $(HORIZONTAL_MICROSERVICE_PATTERN_PATH)/$(DOCKERFILE).service.virginica \
		.
	
.PHONY: run_horizontal_microservice_pattern_virginica
run_horizontal_microservice_pattern_virginica:
	docker run \
		-d \
		--name $(HORIZONTAL_MICROSERVICE_PATTERN)_virginica \
		-e MODE:virginica \
		-e PORT:$(HORIZONTAL_MICROSERVICE_PATTERN_VIRGINICA_PORT) \
		-p $(HORIZONTAL_MICROSERVICE_PATTERN_VIRGINICA_PORT):$(HORIZONTAL_MICROSERVICE_PATTERN_VIRGINICA_PORT) \
		$(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_virginica_$(IMAGE_VERSION)

.PHONY: stop_horizontal_microservice_pattern_virginica
stop_horizontal_microservice_pattern_virginica:
	docker rm -f $(HORIZONTAL_MICROSERVICE_PATTERN)_virginica


.PHONY: build_horizontal_microservice_pattern_proxy
build_horizontal_microservice_pattern_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_proxy_$(IMAGE_VERSION) \
		-f $(HORIZONTAL_MICROSERVICE_PATTERN_PATH)/$(DOCKERFILE).proxy \
		.
	
.PHONY: run_horizontal_microservice_pattern_proxy
run_horizontal_microservice_pattern_proxy:
	docker run \
		-d \
		--name $(HORIZONTAL_MICROSERVICE_PATTERN)_proxy \
		-e MODE:proxy \
		-e PORT:$(HORIZONTAL_MICROSERVICE_PATTERN_PROXY_PORT) \
		-p $(HORIZONTAL_MICROSERVICE_PATTERN_PROXY_PORT):$(HORIZONTAL_MICROSERVICE_PATTERN_PROXY_PORT) \
		$(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_proxy_$(IMAGE_VERSION)

.PHONY: stop_horizontal_microservice_pattern_proxy
stop_horizontal_microservice_pattern_proxy:
	docker rm -f $(HORIZONTAL_MICROSERVICE_PATTERN)_proxy

.PHONY: build_horizontal_microservice_pattern
build_horizontal_microservice_pattern:
	docker-compose \
		-f $(HORIZONTAL_MICROSERVICE_PATTERN)/$(DOCKER_COMPOSE) \
		build

.PHONY: up_horizontal_microservice_pattern
up_horizontal_microservice_pattern:
	docker-compose \
		-f $(HORIZONTAL_MICROSERVICE_PATTERN)/$(DOCKER_COMPOSE) \
		up -d

.PHONY: down_horizontal_microservice_pattern
down_horizontal_microservice_pattern:
	docker-compose \
		-f $(HORIZONTAL_MICROSERVICE_PATTERN)/$(DOCKER_COMPOSE) \
		down


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

.PHONY: build_sync_async_pattern_proxy
build_sync_async_pattern_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_PROXY)_$(IMAGE_VERSION) \
		-f $(SYNC_ASYNC_PATTERN)/$(DOCKERFILE).proxy .

.PHONY: run_sync_async_pattern_proxy
run_sync_async_pattern_proxy:
	docker run \
		-d \
		--name $(SYNC_ASYNC_PATTERN_PROXY) \
		-p $(SYNC_ASYNC_PATTERN_PROXY_PORT):$(SYNC_ASYNC_PATTERN_PROXY_PORT) \
		$(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_PROXY)_$(IMAGE_VERSION)

.PHONY: build_sync_async_pattern_sync
build_sync_async_pattern_sync:
	docker build \
		-t $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_SYNC_MODEL)_$(IMAGE_VERSION) \
		-f $(SYNC_ASYNC_PATTERN)/$(SYNC_ASYNC_PATTERN_SYNC_MODEL)/$(DOCKERFILE) .

.PHONY: run_sync_async_pattern_sync
run_sync_async_pattern_sync:
	docker run \
		-d \
		--name $(SYNC_ASYNC_PATTERN_SYNC_MODEL) \
		-p $(SYNC_ASYNC_PATTERN_SYNC_GRPC_PORT):$(SYNC_ASYNC_PATTERN_SYNC_GRPC_PORT) \
		-p $(SYNC_ASYNC_PATTERN_SYNC_REST_PORT):$(SYNC_ASYNC_PATTERN_SYNC_REST_PORT) \
		$(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_SYNC_MODEL)_$(IMAGE_VERSION)

.PHONY: build_sync_async_pattern_async
build_sync_async_pattern_async:
	docker build \
		-t $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_ASYNC_MODEL)_$(IMAGE_VERSION) \
		-f $(SYNC_ASYNC_PATTERN)/$(SYNC_ASYNC_PATTERN_ASYNC_MODEL)/$(DOCKERFILE) .

.PHONY: run_sync_async_pattern_async
run_sync_async_pattern_async:
	docker run \
		-d \
		--name $(SYNC_ASYNC_PATTERN_ASYNC_MODEL) \
		-p $(SYNC_ASYNC_PATTERN_ASYNC_GRPC_PORT):$(SYNC_ASYNC_PATTERN_ASYNC_GRPC_PORT) \
		-p $(SYNC_ASYNC_PATTERN_ASYNC_REST_PORT):$(SYNC_ASYNC_PATTERN_ASYNC_REST_PORT) \
		$(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_ASYNC_MODEL)_$(IMAGE_VERSION)

.PHONY: build_sync_async_pattern_backend
build_sync_async_pattern_backend:
	docker build \
		-t $(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_BACKEND)_$(IMAGE_VERSION) \
		-f $(SYNC_ASYNC_PATTERN)/$(DOCKERFILE).backend .

.PHONY: run_sync_async_pattern_backend
run_sync_async_pattern_backend:
	docker run \
		-d \
		--name $(SYNC_ASYNC_PATTERN_BACKEND) \
		$(DOCKER_REPOSITORY):$(SYNC_ASYNC_PATTERN)_$(SYNC_ASYNC_PATTERN_BACKEND)_$(IMAGE_VERSION)

.PHONY: build_sync_async_pattern
build_sync_async_pattern:
	docker-compose \
		-f $(SYNC_ASYNC_PATTERN)/$(DOCKER_COMPOSE) \
		build

.PHONY: up_sync_async_pattern
up_sync_async_pattern:
	docker-compose \
		-f $(SYNC_ASYNC_PATTERN)/$(DOCKER_COMPOSE) \
		up -d

.PHONY: down_sync_async_pattern
down_sync_async_pattern:
	docker-compose \
		-f $(SYNC_ASYNC_PATTERN)/$(DOCKER_COMPOSE) \
		down