DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1

PREP_PRED_PATTERN := prep_pred_pattern
PREP_PRED_PATTERN_PREP := prep
PREP_PRED_PATTERN_PREP_PORT := 8000
PREP_PRED_PATTERN_PRED := pred
PREP_PRED_PATTERN_REST_PORT := 8001
PREP_PRED_PATTERN_GRPC_PORT := 50051

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

.PHONY: build_prep
build_prep:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(PREP_PRED_PATTERN_PREP)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).prep .

.PHONY: push_prep
push_prep: 
	docker push $(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(PREP_PRED_PATTERN_PREP)_$(IMAGE_VERSION)

.PHONY: build_pred
build_pred:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(PREP_PRED_PATTERN_PRED)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).pred .

.PHONY: push_pred
push_pred:
	docker push $(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(PREP_PRED_PATTERN_PRED)_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build_prep build_pred

.PHONY: push_all
push_all: push_prep push_pred

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


