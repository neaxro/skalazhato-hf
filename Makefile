export CLUSTER_NAME=skalazhato-hf-local-dev

.PHONY: help
help: ## Show this help message with available targets and descriptions.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: cluster-create
cluster-create: ## Creates kind cluster using config file.
	kind create cluster --config=kind.yaml

.PHONY: cluster-delete
cluster-delete: ## Deletes kind cluster.
	kind delete cluster --name $(CLUSTER_NAME)

.PHONY: cluster-kubeconfig
cluster-kubeconfig: ## Exports and sets the kubeconfig of the kind cluster.
	kind export kubeconfig --name $(CLUSTER_NAME)
