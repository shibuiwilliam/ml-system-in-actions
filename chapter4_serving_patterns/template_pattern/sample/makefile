DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
IMAGE_VERSION := 0.0.1

TEMPLATE_PATTERN := sample
TEMPLATE_PATTERN_PORT := 8000


.PHONY: build
build:
	docker build \
		-t $(DOCKER_REPOSITORY):$(TEMPLATE_PATTERN)_$(IMAGE_VERSION) \
		-f $(DOCKERFILE) \
		.
	 
.PHONY: run
run:
	docker run \
		-d \
		--name $(TEMPLATE_PATTERN) \
		-p $(TEMPLATE_PATTERN_PORT):$(TEMPLATE_PATTERN_PORT) \
		$(DOCKER_REPOSITORY):$(TEMPLATE_PATTERN)_$(IMAGE_VERSION)

.PHONY: stop
stop:
	docker rm -f $(TEMPLATE_PATTERN)

.PHONY: push
push:
	docker push $(DOCKER_REPOSITORY):$(TEMPLATE_PATTERN)_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build

.PHONY: run_all
run_all: run

.PHONY: push_all
push_all: push