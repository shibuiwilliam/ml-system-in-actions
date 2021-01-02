DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
IMAGE_VERSION := 0.0.1

PREDICTION_LOG_PATTERN := prediction_log_pattern
PREDICTION_LOG_PATTERN_PORT := 8000


.PHONY: build_api
build_api:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_LOG_PATTERN)_api_$(IMAGE_VERSION) \
		-f $(DOCKERFILE).api \
		.
	 

.PHONY: push_api
push_api:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_LOG_PATTERN)_api_$(IMAGE_VERSION)


.PHONY: build_client
build_client:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_LOG_PATTERN)_client_$(IMAGE_VERSION) \
		-f $(DOCKERFILE).client \
		.

.PHONY: push_client
push_client:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_LOG_PATTERN)_client_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build_api build_client


.PHONY: push_all
push_all: push_api push_client

.PHONY: deploy
deploy:
	kubectl apply -f manifests/namespace.yml
	kubectl apply -f manifests/
