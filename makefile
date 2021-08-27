_absolute_path := $(shell pwd)

.PHONY: install_prettier
install_prettier:
	npm install

.PHONY: format_md
format_md: 
	npx prettier --write .

.PHONY: dev_sync
dev_sync:
	pipenv sync --dev

.PHONY: dev
dev:
	pip install pipenv
	PIPENV_VENV_IN_PROJECT=true pipenv shell

.PHONY: sync
sync:
	pipenv sync

.PHONY: fmt
fmt: format_md
	pipenv run sort
	pipenv run fmt

.PHONY: lint
lint:
	pipenv run lint
	npx prettier --check .

.PHONY: vet
vet:
	pipenv run vet

.PHONY: build_all
build_all:
	@cd chapter2_training/model_db && make build_all
	@cd chapter3_release_patterns/model_in_image_pattern && make build_all
	@cd chapter3_release_patterns/model_load_pattern && make build_all
	@cd chapter4_serving_patterns/asynchronous_pattern && make build_all
	@cd chapter4_serving_patterns/batch_pattern && make build_all
	@cd chapter4_serving_patterns/data_cache_pattern && make build_all
	@cd chapter4_serving_patterns/horizontal_microservice_pattern && make build_all
	@cd chapter4_serving_patterns/prediction_cache_pattern && make build_all
	@cd chapter4_serving_patterns/prep_pred_pattern && make build_all
	@cd chapter4_serving_patterns/sync_async_pattern && make build_all
	@cd chapter4_serving_patterns/synchronous_pattern && make build_all
	@cd chapter4_serving_patterns/web_single_pattern && make build_all
	@cd chapter5_operations/prediction_log_pattern && make build_all
	@cd chapter5_operations/prediction_monitoring_pattern && make build_all
	@cd chapter6_operation_management/circuit_breaker_pattern && make build_all
	@cd chapter6_operation_management/condition_based_pattern && make build_all
	@cd chapter6_operation_management/load_test_pattern && make build_all
	@cd chapter6_operation_management/online_ab_pattern && make build_all
	@cd chapter6_operation_management/paramater_based_pattern && make build_all
	@cd chapter6_operation_management/shadow_ab_pattern && make build_all

.PHONY: push_all
push_all:
	@cd chapter2_training/model_db && make push_all
	@cd chapter3_release_patterns/model_in_image_pattern && make push_all
	@cd chapter3_release_patterns/model_load_pattern && make push_all
	@cd chapter4_serving_patterns/asynchronous_pattern && make push_all
	@cd chapter4_serving_patterns/batch_pattern && make push_all
	@cd chapter4_serving_patterns/data_cache_pattern && make push_all
	@cd chapter4_serving_patterns/horizontal_microservice_pattern && make push_all
	@cd chapter4_serving_patterns/prediction_cache_pattern && make push_all
	@cd chapter4_serving_patterns/prep_pred_pattern && make push_all
	@cd chapter4_serving_patterns/sync_async_pattern && make push_all
	@cd chapter4_serving_patterns/synchronous_pattern && make push_all
	@cd chapter4_serving_patterns/web_single_pattern && make push_all
	@cd chapter5_operations/prediction_log_pattern && make push_all
	@cd chapter5_operations/prediction_monitoring_pattern && make push_all
	@cd chapter6_operation_management/circuit_breaker_pattern && make push_all
	@cd chapter6_operation_management/condition_based_pattern && make push_all
	@cd chapter6_operation_management/load_test_pattern && make push_all
	@cd chapter6_operation_management/online_ab_pattern && make push_all
	@cd chapter6_operation_management/paramater_based_pattern && make push_all
	@cd chapter6_operation_management/shadow_ab_pattern && make push_all

