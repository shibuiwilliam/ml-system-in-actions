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

