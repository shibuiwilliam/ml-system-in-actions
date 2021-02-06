DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1

PREDICTION_CACHE_PATTERN := prediction_cache_pattern
PREDICTION_CACHE_PATTERN_PREP := proxy
PREDICTION_CACHE_PATTERN_PREP_PORT := 8000
PREDICTION_CACHE_PATTERN_PRED := pred
PREDICTION_CACHE_PATTERN_REST_PORT := 8001
PREDICTION_CACHE_PATTERN_GRPC_PORT := 50051

.PHONY: proto
proto:
	python \
		-m grpc_tools.protoc \
		-I src/proto \
		--python_out=src/proto \
		--grpc_python_out=src/proto \
		src/proto/onnx-ml.proto \
		src/proto/predict.proto \
		src/proto/prediction_service.proto

.PHONY: build_proxy
build_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PREP)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).proxy .

.PHONY: push_proxy
push_proxy:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PREP)_$(IMAGE_VERSION)

.PHONY: build_pred
build_pred:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PRED)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).pred .

.PHONY: push_pred 
push_pred:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PRED)_$(IMAGE_VERSION)


.PHONY: build_all
build_all: build_proxy build_pred


.PHONY: push_all
push_all: push_proxy push_pred

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

