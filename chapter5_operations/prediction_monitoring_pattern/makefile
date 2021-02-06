DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1

PREDICTION_MONITORING_PATTERN := prediction_monitoring_pattern
PREDICTION_MONITORING_PATTERN_PORT := 8000


.PHONY: build_api
build_api:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_MONITORING_PATTERN)_api_$(IMAGE_VERSION) \
		-f $(DOCKERFILE).api \
		.
	 

.PHONY: push_api
push_api:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_MONITORING_PATTERN)_api_$(IMAGE_VERSION)


.PHONY: build_job
build_job:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_MONITORING_PATTERN)_job_$(IMAGE_VERSION) \
		-f $(DOCKERFILE).job \
		.

.PHONY: push_job
push_job:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_MONITORING_PATTERN)_job_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build_api build_job


.PHONY: push_all
push_all: push_api push_job

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

.PHONY: predict
predict:
	curl \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
		localhost:8000/predict
