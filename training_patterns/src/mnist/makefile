_absolute_path := $(shell pwd)
_base_image_name := shibui/ml-system-in-action
_traininig_pattern := training_pattern

dockerfile := Dockerfile
docker_build := docker build \
	-t $(_base_image_name):$(_traininig_pattern)_mnist_0.0.1 \
	-f $(dockerfile) .

.PHONY: d_build
d_build:
	$(docker_build)

.PHONY: train
train:
	mlflow run .  --no-conda

.PHONY: ui
ui:
	mlflow ui
