DOCKER_REPOSITORY := shibui/ml-system-in-action

ABSOLUTE_PATH := $(shell pwd)

WEB_SERVING_PATTERN := web_single_pattern
WEB_SERVING_PATTERN_PATH := $(ABSOLUTE_PATH)/$(WEB_SERVING_PATTERN)
WEB_SERVING_PATTERN_PORT := 8000

.PHONY: build_web_serving_pattern
build_web_serving_pattern:
	docker build \
		-t ${DOCKER_REPOSITORY}:${WEB_SERVING_PATTERN} \
		-f ${WEB_SERVING_PATTERN_PATH}/Dockerfile \
		.
	
.PHONY: run_web_serving_pattern
run_web_serving_pattern:
	docker run \
		-d \
		--rm \
		--name ${WEB_SERVING_PATTERN} \
		-p ${WEB_SERVING_PATTERN_PORT}:${WEB_SERVING_PATTERN_PORT} \
		${DOCKER_REPOSITORY}:${WEB_SERVING_PATTERN}

.PHONY: stop_web_serving_pattern
stop_web_serving_pattern:
	docker rm -f ${WEB_SERVING_PATTERN}

.PHONY: push_web_serving_pattern
push_web_serving_pattern:
	docker push ${DOCKER_REPOSITORY}:${WEB_SERVING_PATTERN}