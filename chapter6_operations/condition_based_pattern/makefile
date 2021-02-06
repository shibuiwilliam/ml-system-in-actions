DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1


CONDITION_BASED_PATTERN := condition_based_pattern
CONDITION_BASED_PATTERN_PATH := $(ABSOLUTE_PATH)/$(CONDITION_BASED_PATTERN)

CONDITION_BASED_PATTERN_MOBILENET_V2 := imagenet_mobilenet_v2
CONDITION_BASED_PATTERN_PLANT := plant

CONDITION_BASED_PATTERN_MOBILENET_V2_PROXY_PORT := 8000
CONDITION_BASED_PATTERN_PLANT_PROXY_PORT := 9000

CONDITION_BASED_PATTERN_MOBILENET_V2_GRPC_PORT := 8500
CONDITION_BASED_PATTERN_MOBILENET_V2_REST_PORT := 8501
CONDITION_BASED_PATTERN_PLANT_GRPC_PORT := 9500
CONDITION_BASED_PATTERN_PLANT_REST_PORT := 9501

.PHONY: build_proxy
build_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(CONDITION_BASED_PATTERN)_proxy_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).proxy \
		.

.PHONY: push_proxy
push_proxy:
	docker push $(DOCKER_REPOSITORY):$(CONDITION_BASED_PATTERN)_proxy_$(IMAGE_VERSION)


.PHONY: build_mobilenet_v2
build_mobilenet_v2:
	docker build \
		-t $(DOCKER_REPOSITORY):$(CONDITION_BASED_PATTERN)_$(CONDITION_BASED_PATTERN_MOBILENET_V2)_$(IMAGE_VERSION) \
		-f ./$(CONDITION_BASED_PATTERN_MOBILENET_V2)/$(DOCKERFILE) .

.PHONY: push_mobilenet_v2
push_mobilenet_v2:
	docker push $(DOCKER_REPOSITORY):$(CONDITION_BASED_PATTERN)_$(CONDITION_BASED_PATTERN_MOBILENET_V2)_$(IMAGE_VERSION)


.PHONY: build_plant
build_plant:
	docker build \
		-t $(DOCKER_REPOSITORY):$(CONDITION_BASED_PATTERN)_$(CONDITION_BASED_PATTERN_PLANT)_$(IMAGE_VERSION) \
		-f ./$(CONDITION_BASED_PATTERN_PLANT)/$(DOCKERFILE) .

.PHONY: push_plant
push_plant:
	docker push $(DOCKER_REPOSITORY):$(CONDITION_BASED_PATTERN)_$(CONDITION_BASED_PATTERN_PLANT)_$(IMAGE_VERSION)


.PHONY: build_client
build_client:
	docker build \
		-t $(DOCKER_REPOSITORY):$(CONDITION_BASED_PATTERN)_client_$(IMAGE_VERSION) \
		-f $(DOCKERFILE).client \
		.

.PHONY: push_client
push_client:
	docker push $(DOCKER_REPOSITORY):$(CONDITION_BASED_PATTERN)_client_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build_proxy build_mobilenet_v2 build_plant build_client


.PHONY: push_all
push_all: push_proxy push_mobilenet_v2 push_plant push_client

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

.PHONY: deploy
deploy:
	istioctl install -y
	kubectl apply -f manifests/namespace.yml
	kubectl apply -f manifests/

