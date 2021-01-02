DOCKER_REPOSITORY := shibui/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
IMAGE_VERSION := 0.0.1

WEB_SINGLE_PATTERN := web_single_pattern
WEB_SINGLE_PATTERN_PORT := 8000


.PHONY: build
build:
	docker build \
		-t $(DOCKER_REPOSITORY):$(WEB_SINGLE_PATTERN)_$(IMAGE_VERSION) \
		-f $(DOCKERFILE) \
		.
	 
.PHONY: run
run:
	docker run \
		-d \
		--name $(WEB_SINGLE_PATTERN) \
		-p $(WEB_SINGLE_PATTERN_PORT):$(WEB_SINGLE_PATTERN_PORT) \
		$(DOCKER_REPOSITORY):$(WEB_SINGLE_PATTERN)_$(IMAGE_VERSION)

.PHONY: stop
stop:
	docker rm -f $(WEB_SINGLE_PATTERN)

.PHONY: push
push:
	docker push $(DOCKER_REPOSITORY):$(WEB_SINGLE_PATTERN)_$(IMAGE_VERSION)

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
		-d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
		localhost:8000/predict

.PHONY: predict_label
predict_label:
	curl \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
		localhost:8000/predict/label