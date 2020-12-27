_absolute_path := $(shell pwd)
_dockerfile_dir := dockerfiles

_train_iris_batch_container_file := Dockerfile_train_iris_batch
_train_iris_batch_image_name := training_patterns_train_iris_batch
_train_iris_batch_image_version := latest
_train_iris_batch_container_name := training_patterns_train_iris_batch
_train_iris_batch_model_path := $(_absolute_path)/src/iris_batch/models
_train_iris_batch_data_path := $(_absolute_path)/src/iris_batch/data

_train_iris_pipeline_container_file := Dockerfile_train_iris_pipeline
_train_iris_pipeline_image_name := training_patterns_train_iris_pipeline
_train_iris_pipeline_image_version := latest
_work_dir := $(_absolute_path)/src/iris_pipeline/

_build_train_iris_batch := \
	docker build \
		-t $(_train_iris_batch_image_name):$(_train_iris_batch_image_version) \
		-f $(_dockerfile_dir)/$(_train_iris_batch_container_file) .

_run_train_iris_batch := \
	docker run --rm \
		--name $(_train_iris_batch_container_name) \
		-v $(_train_iris_batch_model_path):/training_patterns/src/iris_batch/models \
		-v $(_train_iris_batch_data_path):/training_pattern/src/iris_batch/data \
		$(_train_iris_batch_image_name):$(_train_iris_batch_image_version)

_build_train_iris_pipeline := \
	docker build \
		-t $(_train_iris_pipeline_image_name):$(_train_iris_pipeline_image_version) \
		-f $(_dockerfile_dir)/$(_train_iris_pipeline_container_file) .

_run_train_iris_pipeline := \
	cd $(_work_dir) && \
	./run_dvc.sh


.PHONY: build_train_iris_batch
build_train_iris_batch:
	$(_build_train_iris_batch)

.PHONY: run_train_iris_batch
run_train_iris_batch:
	$(_run_train_iris_batch)

.PHONY: train_iris_batch
train_iris_batch: build_train_iris_batch run_train_iris_batch

.PHONY: build_train_iris_pipeline
build_train_iris_pipeline:
	$(_build_train_iris_pipeline)

.PHONY: run_train_iris_pipeline
run_train_iris_pipeline:
	$(_run_train_iris_pipeline)

.PHONY: train_iris_pipeline
train_iris_pipeline: build_train_iris_pipeline run_train_iris_pipeline
