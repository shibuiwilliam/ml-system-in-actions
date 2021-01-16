DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1


HORIZONTAL_MICROSERVICE_PATTERN := horizontal_microservice_pattern
HORIZONTAL_MICROSERVICE_PATTERN_PATH := $(ABSOLUTE_PATH)/$(HORIZONTAL_MICROSERVICE_PATTERN)
HORIZONTAL_MICROSERVICE_PATTERN_SETOSA_PORT := 8000
HORIZONTAL_MICROSERVICE_PATTERN_VERSICOLOR_PORT := 8001
HORIZONTAL_MICROSERVICE_PATTERN_VIRGINICA_PORT := 8002

HORIZONTAL_MICROSERVICE_PATTERN_PROXY_PORT := 9000

.PHONY: build_setosa
build_setosa:
	docker build \
		-t $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_setosa_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).service.setosa \
		.
	
.PHONY: stop_setosa
stop_setosa:
	docker rm -f $(HORIZONTAL_MICROSERVICE_PATTERN)_setosa


.PHONY: push_setosa
push_setosa:
	docker push $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_setosa_$(IMAGE_VERSION)


.PHONY: build_versicolor
build_versicolor:
	docker build \
		-t $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_versicolor_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).service.versicolor \
		.
	
.PHONY: stop_versicolor
stop_versicolor:
	docker rm -f $(HORIZONTAL_MICROSERVICE_PATTERN)_versicolor

.PHONY: push_versicolor
push_versicolor:
	docker push $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_versicolor_$(IMAGE_VERSION)


.PHONY: build_virginica
build_virginica:
	docker build \
		-t $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_virginica_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).service.virginica \
		.
	
.PHONY: stop_virginica
stop_virginica:
	docker rm -f $(HORIZONTAL_MICROSERVICE_PATTERN)_virginica

.PHONY: push_virginica
push_virginica:
	docker push $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_virginica_$(IMAGE_VERSION)


.PHONY: build_proxy
build_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_proxy_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).proxy \
		.
	
.PHONY: stop_proxy
stop_proxy:
	docker rm -f $(HORIZONTAL_MICROSERVICE_PATTERN)_proxy

.PHONY: push_proxy
push_proxy:
	docker push $(DOCKER_REPOSITORY):$(HORIZONTAL_MICROSERVICE_PATTERN)_proxy_$(IMAGE_VERSION)


.PHONY: build_all
build_all: build_setosa build_versicolor build_virginica build_proxy


.PHONY: stop_all
stop_all: stop_setosa stop_versicolor stop_virginica stop_proxy

.PHONY: push_all
push_all: push_setosa push_versicolor push_virginica push_proxy

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


.PHONY: health
health:
	curl localhost:9000/health

.PHONY: health_all
health_all:
	curl localhost:9000/health/all

.PHONY: metadata
metadata:
	curl localhost:9000/metadata


.PHONY: predict_get_test
predict_get_test:
	curl localhost:9000/predict/get/test

.PHONY: predict_post_test
predict_post_test:
	curl localhost:9000/predict/post/test


.PHONY: predict
predict:
	curl \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
		localhost:9000/predict

.PHONY: predict_label
predict_label:
	curl \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
		localhost:9000/predict/label
