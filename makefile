_absolute_path := $(shell pwd)

.PHONY: dev_sync
dev_sync:
	pipenv sync --dev

.PHONY: dev
dev:
	pip install pipenv
	PIPENV_VENV_IN_PROJECT=true pipenv shell
	$(dev_sync)

.PHONY: sync
sync:
	pipenv sync

.PHONY: fmt
fmt:
	pipenv run sort
	pipenv run fmt
	npx prettier --write .

.PHONY: lint
lint:
	pipenv run lint
	npx prettier --check .

.PHONY: vet
vet:
	pipenv run vet