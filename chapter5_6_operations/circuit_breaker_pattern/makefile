DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
IMAGE_VERSION := 0.0.1

CIRCUIT_BREAKER_PATTERN := circuit_breaker_pattern
CIRCUIT_BREAKER_PATTERN_PORT := 8000
MODEL_LOADER := model_loader


.PHONY: build_api
build_api:
	docker build \
		-t $(DOCKER_REPOSITORY):$(CIRCUIT_BREAKER_PATTERN)_api_$(IMAGE_VERSION) \
		-f $(DOCKERFILE) \
		.

.PHONY: push_api
push_api:
	docker push $(DOCKER_REPOSITORY):$(CIRCUIT_BREAKER_PATTERN)_api_$(IMAGE_VERSION)

.PHONY: build_loader
build_loader:
	docker build \
		-t $(DOCKER_REPOSITORY):$(CIRCUIT_BREAKER_PATTERN)_loader_$(IMAGE_VERSION) \
		-f $(MODEL_LOADER)/$(DOCKERFILE) \
		.

.PHONY: push_loader
push_loader:
	docker push $(DOCKER_REPOSITORY):$(CIRCUIT_BREAKER_PATTERN)_loader_$(IMAGE_VERSION) 


.PHONY: build_client
build_client:
	docker build \
		-t $(DOCKER_REPOSITORY):$(CIRCUIT_BREAKER_PATTERN)_client_$(IMAGE_VERSION) \
		-f $(DOCKERFILE).client \
		.

.PHONY: push_client
push_client:
	docker push $(DOCKER_REPOSITORY):$(CIRCUIT_BREAKER_PATTERN)_client_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build_api build_loader build_client

.PHONY: push_all
push_all: push_api push_loader push_client

.PHONY: deploy
deploy:
	istioctl install -y
	kubectl apply -f manifests/namespace.yml
	kubectl apply -f manifests/


