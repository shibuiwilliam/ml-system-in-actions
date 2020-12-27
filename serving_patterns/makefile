_absolute_path := $(shell pwd)
_dockerfile_dir := dockerfiles
_dockercompose_dir := docker-composes

_image_name := serving_patterns_api
_image_version := latest
_container_name := serving_patterns_api

_test_dir := tests
_test_container_file := Dockerfile_test
_test_image_version := test
_test_container_name := test

_extract_resnet50_onnx_work_dir := src/app/ml/resnet50_onnx
_extract_resnet50_onnx_container_file := Dockerfile_extract_resnet50_onnx
_extract_resnet50_onnx_image_name := serving_patterns_extract_resnet50_onnx
_extract_resnet50_onnx_image_version := latest
_extract_resnet50_onnx_container_name := serving_patterns_extract_resnet50_onnx

_extract_resnet50_onnx_server_work_dir := src/app/ml/resnet50_onnx_server
_extract_resnet50_onnx_server_container_file := Dockerfile_extract_resnet50_onnx_server
_extract_resnet50_onnx_server_image_name := serving_patterns_extract_resnet50_onnx_server
_extract_resnet50_onnx_server_image_version := latest
_extract_resnet50_onnx_server_container_name := serving_patterns_extract_resnet50_onnx_server

_extract_resnet50_tfs_work_dir := src/app/ml/resnet50_tfs
_extract_resnet50_tfs_container_file := Dockerfile_extract_resnet50_tfs
_extract_resnet50_tfs_image_name := serving_patterns_extract_resnet50_tfs
_extract_resnet50_tfs_image_version := latest
_extract_resnet50_tfs_container_name := serving_patterns_extract_resnet50_tfs

_extract_inceptionv3_tfs_work_dir := src/app/ml/inceptionv3
_extract_inceptionv3_container_file := Dockerfile_extract_inceptionv3
_extract_inceptionv3_image_name := serving_patterns_extract_inceptionv3
_extract_inceptionv3_image_version := latest
_extract_inceptionv3_container_name := serving_patterns_extract_inceptionv3

_extract_mobilenetv2_tfs_work_dir := src/app/ml/mobilenetv2
_extract_mobilenetv2_container_file := Dockerfile_extract_mobilenetv2
_extract_mobilenetv2_image_name := serving_patterns_extract_mobilenetv2
_extract_mobilenetv2_image_version := latest
_extract_mobilenetv2_container_name := serving_patterns_extract_mobilenetv2

_extract_mobilenetv2_plant_tfs_work_dir := src/app/ml/mobilenetv2_plant
_extract_mobilenetv2_plant_container_file := Dockerfile_extract_mobilenetv2_plant
_extract_mobilenetv2_plant_image_name := serving_patterns_extract_mobilenetv2_plant
_extract_mobilenetv2_plant_image_version := latest
_extract_mobilenetv2_plant_container_name := serving_patterns_extract_mobilenetv2_plant

_c_api := $(_dockercompose_dir)/docker-compose_api.yml
_c_build_api := docker-compose -f $(_c_api) build
_c_up_api := docker-compose -f $(_c_api) up -d
_c_down_api := docker-compose -f $(_c_api) down

_c_resnet50_onnx := $(_dockercompose_dir)/docker-compose_resnet50_onnx.yml
_c_build_resnet50_onnx := docker-compose -f $(_c_resnet50_onnx) build
_c_up_resnet50_onnx := docker-compose -f $(_c_resnet50_onnx) up -d
_c_down_resnet50_onnx := docker-compose -f $(_c_resnet50_onnx) down

_c_resnet50_onnx_server := $(_dockercompose_dir)/docker-compose_resnet50_onnx_server.yml
_c_build_resnet50_onnx_server := docker-compose -f $(_c_resnet50_onnx_server) build
_c_up_resnet50_onnx_server := docker-compose -f $(_c_resnet50_onnx_server) up -d
_c_down_resnet50_onnx_server := docker-compose -f $(_c_resnet50_onnx_server) down

_c_resnet50_tfs := $(_dockercompose_dir)/docker-compose_resnet50_tfs.yml
_c_build_resnet50_tfs := docker-compose -f $(_c_resnet50_tfs) build
_c_up_resnet50_tfs := docker-compose -f $(_c_resnet50_tfs) up -d
_c_down_resnet50_tfs := docker-compose -f $(_c_resnet50_tfs) down

_c_inceptionv3 := $(_dockercompose_dir)/docker-compose_inceptionv3.yml
_c_build_inceptionv3 := docker-compose -f $(_c_inceptionv3) build
_c_up_inceptionv3 := docker-compose -f $(_c_inceptionv3) up -d
_c_down_inceptionv3 := docker-compose -f $(_c_inceptionv3) down

_c_mobilenetv2 := $(_dockercompose_dir)/docker-compose_mobilenetv2.yml
_c_build_mobilenetv2 := docker-compose -f $(_c_mobilenetv2) build
_c_up_mobilenetv2 := docker-compose -f $(_c_mobilenetv2) up -d
_c_down_mobilenetv2 := docker-compose -f $(_c_mobilenetv2) down

_c_mobilenetv2_plant := $(_dockercompose_dir)/docker-compose_mobilenetv2_plant.yml
_c_build_mobilenetv2_plant := docker-compose -f $(_c_mobilenetv2_plant) build
_c_up_mobilenetv2_plant := docker-compose -f $(_c_mobilenetv2_plant) up -d
_c_down_mobilenetv2_plant := docker-compose -f $(_c_mobilenetv2_plant) down

_c_api_ms_horizontal := $(_dockercompose_dir)/docker-compose_api_ms_horizontal.yml
_c_build_api_ms_horizontal := docker-compose -f $(_c_api_ms_horizontal) build
_c_up_api_ms_horizontal := docker-compose -f $(_c_api_ms_horizontal) up -d
_c_down_api_ms_horizontal := docker-compose -f $(_c_api_ms_horizontal) down

_c_image_ms_horizontal := $(_dockercompose_dir)/docker-compose_image_ms_horizontal.yml
_c_build_image_ms_horizontal := docker-compose -f $(_c_image_ms_horizontal) build
_c_up_image_ms_horizontal := docker-compose -f $(_c_image_ms_horizontal) up -d
_c_down_image_ms_horizontal := docker-compose -f $(_c_image_ms_horizontal) down

_c_resnet50_load_test := $(_dockercompose_dir)/docker-compose_resnet50_load_test.yml
_c_build_resnet50_load_test := docker-compose -f $(_c_resnet50_load_test) build
_c_up_resnet50_load_test := docker-compose -f $(_c_resnet50_load_test) up -d
_c_down_resnet50_load_test := docker-compose -f $(_c_resnet50_load_test) down

_c_api_ab_test := $(_dockercompose_dir)/docker-compose_api_ab_test.yml
_c_build_api_ab_test := docker-compose -f $(_c_api_ab_test) build
_c_up_api_ab_test := docker-compose -f $(_c_api_ab_test) up -d
_c_down_api_ab_test := docker-compose -f $(_c_api_ab_test) down

_requirements_test := requirements_test.txt
_pip_freeze_test := pip freeze > requirements/$(_requirements_test)
_pip_install_test := pip install  --no-cache-dir -r requirements/$(_requirements_test)

_test_request_api := ./scripts/test_request_api.sh
_test_request_resnet50_onnx := ./scripts/test_request_resnet50_onnx.sh
_test_request_inceptionv3 := ./scripts/test_request_inceptionv3.sh
_test_request_mobilenetv2 := ./scripts/test_request_mobilenetv2.sh
_test_request_image_ms_horizontal := ./scripts/test_request_image_ms_horizontal.sh

_pytest_d := \
	docker build \
		-t $(_image_name):$(_test_image_version) \
		-f $(_absolute_path)/$(_test_dir)/$(_test_container_file) . && \
	docker run --rm \
		--name $(_test_container_name) \
		-v $(_absolute_path)/models/:/serving_patterns/models/ \
		-e PROFILE=0 \
		-e PLATFORM=test \
		$(_image_name):$(_test_image_version) pytest -v -s ./tests/

_extract_resnet50_onnx := \
	docker build \
		-t $(_extract_resnet50_onnx_image_name):$(_extract_resnet50_onnx_image_version) \
		-f $(_absolute_path)/$(_extract_resnet50_onnx_work_dir)/$(_extract_resnet50_onnx_container_file) . && \
	docker run --rm \
		--name $(_extract_resnet50_onnx_container_name) \
		-v $(_absolute_path)/$(_extract_resnet50_onnx_work_dir)/data/:/serving_patterns/$(_extract_resnet50_onnx_work_dir)/data/ \
		-v $(_absolute_path)/$(_extract_resnet50_onnx_work_dir)/model/:/serving_patterns/$(_extract_resnet50_onnx_work_dir)/model/ \
		$(_extract_resnet50_onnx_image_name):$(_extract_resnet50_onnx_image_version)

_extract_resnet50_onnx_server := \
	docker build \
		-t $(_extract_resnet50_onnx_server_image_name):$(_extract_resnet50_onnx_server_image_version) \
		-f $(_absolute_path)/$(_extract_resnet50_onnx_server_work_dir)/$(_extract_resnet50_onnx_server_container_file) . && \
	docker run --rm \
		--name $(_extract_resnet50_onnx_server_container_name) \
		-v $(_absolute_path)/$(_extract_resnet50_onnx_server_work_dir)/data/:/serving_patterns/$(_extract_resnet50_onnx_server_work_dir)/data/ \
		-v $(_absolute_path)/$(_extract_resnet50_onnx_server_work_dir)/model/:/serving_patterns/$(_extract_resnet50_onnx_server_work_dir)/model/ \
		$(_extract_resnet50_onnx_server_image_name):$(_extract_resnet50_onnx_server_image_version)

_extract_resnet50_tfs := \
	docker build \
		-t $(_extract_resnet50_tfs_image_name):$(_extract_resnet50_tfs_image_version) \
		-f $(_absolute_path)/$(_extract_resnet50_tfs_work_dir)/$(_extract_resnet50_tfs_container_file) . && \
	docker run --rm \
		--name $(_extract_resnet50_tfs_container_name) \
		-v $(_absolute_path)/$(_extract_resnet50_tfs_work_dir)/data/:/serving_patterns/$(_extract_resnet50_tfs_work_dir)/data/ \
		-v $(_absolute_path)/$(_extract_resnet50_tfs_work_dir)/model/:/serving_patterns/$(_extract_resnet50_tfs_work_dir)/model/ \
		$(_extract_resnet50_tfs_image_name):$(_extract_resnet50_tfs_image_version)

_extract_inceptionv3 := \
	docker build \
		-t $(_extract_inceptionv3_image_name):$(_extract_inceptionv3_image_version) \
		-f $(_absolute_path)/$(_extract_inceptionv3_tfs_work_dir)/$(_extract_inceptionv3_container_file) . && \
	docker run --rm \
		--name $(_extract_inceptionv3_container_name) \
		-v $(_absolute_path)/$(_extract_inceptionv3_tfs_work_dir)/data/:/serving_patterns/$(_extract_inceptionv3_tfs_work_dir)/data/ \
		-v $(_absolute_path)/$(_extract_inceptionv3_tfs_work_dir)/model/:/serving_patterns/$(_extract_inceptionv3_tfs_work_dir)/model/ \
		$(_extract_inceptionv3_image_name):$(_extract_inceptionv3_image_version)

_extract_mobilenetv2 := \
	docker build \
		-t $(_extract_mobilenetv2_image_name):$(_extract_mobilenetv2_image_version) \
		-f $(_absolute_path)/$(_extract_mobilenetv2_tfs_work_dir)/$(_extract_mobilenetv2_container_file) . && \
	docker run --rm \
		--name $(_extract_mobilenetv2_container_name) \
		-v $(_absolute_path)/$(_extract_mobilenetv2_tfs_work_dir)/data/:/serving_patterns/$(_extract_mobilenetv2_tfs_work_dir)/data/ \
		-v $(_absolute_path)/$(_extract_mobilenetv2_tfs_work_dir)/model/:/serving_patterns/$(_extract_mobilenetv2_tfs_work_dir)/model/ \
		$(_extract_mobilenetv2_image_name):$(_extract_mobilenetv2_image_version)

_extract_mobilenetv2_plant := \
	docker build \
		-t $(_extract_mobilenetv2_plant_image_name):$(_extract_mobilenetv2_plant_image_version) \
		-f $(_absolute_path)/$(_extract_mobilenetv2_plant_tfs_work_dir)/$(_extract_mobilenetv2_plant_container_file) . && \
	docker run --rm \
		--name $(_extract_mobilenetv2_plant_container_name) \
		-v $(_absolute_path)/$(_extract_mobilenetv2_plant_tfs_work_dir)/data/:/serving_patterns/$(_extract_mobilenetv2_plant_tfs_work_dir)/data/ \
		-v $(_absolute_path)/$(_extract_mobilenetv2_plant_tfs_work_dir)/model/:/serving_patterns/$(_extract_mobilenetv2_plant_tfs_work_dir)/model/ \
		$(_extract_mobilenetv2_plant_image_name):$(_extract_mobilenetv2_plant_image_version)

_build_locust := docker build -t locust:latest -f locust_targets/Dockerfile_locust .

.PHONY: pip_freeze
pip_freeze:
	$(_pip_freeze_test)

.PHONY: clean
clean:
	$(_c_down)

.PHONY: c_build_api
c_build_api:
	$(_c_build_api)

.PHONY: c_up_api
c_up_api:
	$(_c_up_api)

.PHONY: c_down_api
c_down_api:
	$(_c_down_api)

.PHONY: c_build_resnet50_onnx
c_build_resnet50_onnx:
	$(_c_build_resnet50_onnx)

.PHONY: c_up_resnet50_onnx
c_up_resnet50_onnx:
	$(_c_up_resnet50_onnx)

.PHONY: c_down_resnet50_onnx
c_down_resnet50_onnx:
	$(_c_down_resnet50_onnx)

.PHONY: c_build_resnet50_onnx_server
c_build_resnet50_onnx_server:
	$(_c_build_resnet50_onnx_server)

.PHONY: c_up_resnet50_onnx_server
c_up_resnet50_onnx_server:
	$(_c_up_resnet50_onnx_server)

.PHONY: c_down_resnet50_onnx_server
c_down_resnet50_onnx_server:
	$(_c_down_resnet50_onnx_server)

.PHONY: c_build_resnet50_tfs
c_build_resnet50_tfs:
	$(_c_build_resnet50_tfs)

.PHONY: c_up_resnet50_tfs
c_up_resnet50_tfs:
	$(_c_up_resnet50_tfs)

.PHONY: c_down_resnet50_tfs
c_down_resnet50_tfs:
	$(_c_down_resnet50_tfs)

.PHONY: c_build_inceptionv3
c_build_inceptionv3:
	$(_c_build_inceptionv3)

.PHONY: c_up_inceptionv3
c_up_inceptionv3:
	$(_c_up_inceptionv3)

.PHONY: c_down_inceptionv3
c_down_inceptionv3:
	$(_c_down_inceptionv3)

.PHONY: c_build_mobilenetv2
c_build_mobilenetv2:
	$(_c_build_mobilenetv2)

.PHONY: c_up_mobilenetv2
c_up_mobilenetv2:
	$(_c_up_mobilenetv2)

.PHONY: c_down_mobilenetv2
c_down_mobilenetv2:
	$(_c_down_mobilenetv2)

.PHONY: c_build_mobilenetv2_plant
c_build_mobilenetv2_plant:
	$(_c_build_mobilenetv2_plant)

.PHONY: c_up_mobilenetv2_plant
c_up_mobilenetv2_plant:
	$(_c_up_mobilenetv2_plant)

.PHONY: c_down_mobilenetv2_plant
c_down_mobilenetv2_plant:
	$(_c_down_mobilenetv2_plant)

.PHONY: c_build_api_ms_h
c_build_api_ms_h:
	$(_c_build_api_ms_horizontal)

.PHONY: c_up_api_ms_h
c_up_api_ms_h:
	$(_c_up_api_ms_horizontal)

.PHONY: c_down_api_ms_h
c_down_api_ms_h:
	$(_c_down_api_ms_horizontal)

.PHONY: c_build_image_ms_h
c_build_image_ms_h:
	$(_c_build_image_ms_horizontal)

.PHONY: c_up_image_ms_h
c_up_image_ms_h:
	$(_c_up_image_ms_horizontal)

.PHONY: c_down_image_ms_h
c_down_image_ms_h:
	$(_c_down_image_ms_horizontal)

.PHONY: c_build_resnet50_load_test
c_build_resnet50_load_test:
	$(_c_build_resnet50_load_test)

.PHONY: c_up_resnet50_load_test
c_up_resnet50_load_test:
	$(_c_up_resnet50_load_test)

.PHONY: c_down_resnet50_load_test
c_down_resnet50_load_test:
	$(_c_down_resnet50_load_test)

.PHONY: c_build_api_ab_test
c_build_api_ab_test:
	$(_c_build_api_ab_test)

.PHONY: c_up_api_ab_test
c_up_api_ab_test:
	$(_c_up_api_ab_test)

.PHONY: c_down_api_ab_test
c_down_api_ab_test:
	$(_c_down_api_ab_test)

.PHONY: test_d
test_d:
	$(_pytest_d)

.PHONY: test_request_api
test_request_api:
	$(_test_request_api)

.PHONY: test_request_resnet50_onnx
test_request_resnet50_onnx:
	$(_test_request_resnet50_onnx)

.PHONY: test_request_inceptionv3
test_request_inceptionv3:
	$(_test_request_inceptionv3)

.PHONY: test_request_mobilenetv2
test_request_mobilenetv2:
	$(_test_request_mobilenetv2)

.PHONY: test_request_image_ms_horizontal
test_request_image_ms_horizontal:
	$(_test_request_image_ms_horizontal)

.PHONY: build_locust
build_locust:
	$(_build_locust)

.PHONY: run_locust
run_locust:
	docker run -it --rm -p 8089:8089 --name locust locust:latest locust -f ${ARGS}

.PHONY: extract_resnet50_onnx
extract_resnet50_onnx:
	$(_extract_resnet50_onnx)

.PHONY: extract_resnet50_onnx_server
extract_resnet50_onnx_server:
	$(_extract_resnet50_onnx_server)

.PHONY: extract_resnet50_tfs
extract_resnet50_tfs:
	$(_extract_resnet50_tfs)

.PHONY: extract_inceptionv3
extract_inceptionv3:
	$(_extract_inceptionv3)

.PHONY: extract_mobilenetv2
extract_mobilenetv2:
	$(_extract_mobilenetv2)

.PHONY: extract_mobilenetv2_plant
extract_mobilenetv2_plant:
	$(_extract_mobilenetv2_plant)

.PHONY: extract_all
extract_all: extract_resnet50_onnx extract_resnet50_tfs extract_inceptionv3 extract_mobilenetv2 extract_mobilenetv2_plant extract_resnet50_onnx_server test_d

.PHONY: build_all
build_all: extract_all c_build_api c_build_resnet50_onnx c_build_resnet50_tfs c_build_inceptionv3 c_build_mobilenetv2 c_build_api_ms_h c_build_image_ms_h c_build_resnet50_onnx_server build_locust
