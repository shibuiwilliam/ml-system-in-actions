DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := dockercompose.yaml
IMAGE_VERSION := 0.0.1

PREDICTION_CACHE_PATTERN := prediction_cache_pattern
PREDICTION_CACHE_PATTERN_PREP := proxy
PREDICTION_CACHE_PATTERN_PREP_PORT := 8000
PREDICTION_CACHE_PATTERN_PRED := pred
PREDICTION_CACHE_PATTERN_REST_PORT := 8001
PREDICTION_CACHE_PATTERN_GRPC_PORT := 50051

.PHONY: build_proxy
build_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PREP)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).proxy .

.PHONY: run_proxy
run_proxy:
	docker run \
		-d \
		--name $(PREDICTION_CACHE_PATTERN_PREP) \
		-p $(PREDICTION_CACHE_PATTERN_PREP_PORT):$(PREDICTION_CACHE_PATTERN_PREP_PORT) \
		$(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PREP)_$(IMAGE_VERSION)

.PHONY: push_proxy
push_proxy:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PREP)_$(IMAGE_VERSION)

.PHONY: build_pred
build_pred:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PRED)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).pred .

.PHONY: run_pred
run_pred:
	docker run \
		-d \
		--name $(PREDICTION_CACHE_PATTERN_PRED) \
		-p $(PREDICTION_CACHE_PATTERN_GRPC_PORT):$(PREDICTION_CACHE_PATTERN_GRPC_PORT) \
		-p $(PREDICTION_CACHE_PATTERN_REST_PORT):$(PREDICTION_CACHE_PATTERN_REST_PORT) \
		$(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PRED)_$(IMAGE_VERSION)

.PHONY: push_pred 
push_pred:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PRED)_$(IMAGE_VERSION)


.PHONY: build_all
build_all: build_proxy build_pred

.PHONY: run_all
run_all: run_proxy run_pred

.PHONY: push_all
push_all: push_proxy push_pred

.PHONY: c_build
c_build:
	docker-compose \
		-f ./$(DOCKER_COMPOSE) \
		build

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


.PHONY: health
health:
	curl localhost:8000/health

.PHONY: metadata
metadata:
	curl localhost:8000/metadata

.PHONY: label
label:
	curl localhost:8000/label

.PHONY: predict_test
predict_test:
	curl localhost:8000/predict/test

.PHONY: predict_test_label
predict_test_label:
	curl localhost:8000/predict/test/label

.PHONY: predict
predict:
	curl \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{"Data": "0000"}' \
		localhost:8000/predict

.PHONY: predict_label
predict_label:
	curl \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{"Data": "0000"}' \
		localhost:8000/predict/label