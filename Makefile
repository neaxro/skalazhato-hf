export CLUSTER_NAME=skalazhato-hf-local-dev

export SKALAZHATO_RELEASE_NAME=skalazhato
export SKALAZHATO_RELEASE_NS=skalazhato-bemutatas

.PHONY: help
help: ## Show this help message with available targets and descriptions.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: cluster-create
cluster-create: ## Creates kind cluster using config file.
	kind create cluster --config=kind.yaml

.PHONY: cluster-recreate
cluster-recreate: cluster-delete cluster-create

.PHONY: cluster-delete
cluster-delete: ## Deletes kind cluster.
	kind delete cluster --name $(CLUSTER_NAME)

.PHONY: cluster-kubeconfig
cluster-kubeconfig: ## Exports and sets the kubeconfig of the kind cluster.
	kind export kubeconfig --name $(CLUSTER_NAME)

.PHONY: build-app-recipe
build-app-recipe: ## Builds recipe app's container image.
	docker build --file src/apps/recipe-service/Dockerfile --tag recipe:local-latest src/apps/recipe-service/ && \
	kind load docker-image recipe:local-latest --name $(CLUSTER_NAME)

.PHONY: helm-install-skalazhato
helm-install-skalazhato: ## Installs a release.
	helm upgrade --install $(SKALAZHATO_RELEASE_NAME) \
		src/helm/skalazhato \
		-n $(SKALAZHATO_RELEASE_NS) \
		--values src/helm/releases/local-values.yaml \
		--set common.ingress.host=$(SKALAZHATO_RELEASE_NAME).nemes.local

.PHONY: helm-uninstall-skalazhato
helm-uninstall-skalazhato: ## Installs a release.
	helm uninstall $(SKALAZHATO_RELEASE_NAME) \
		-n $(SKALAZHATO_RELEASE_NS) \
