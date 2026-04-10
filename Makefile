VERSION := $(shell cat VERSION)
COMMIT_HASH := $(shell git rev-parse HEAD)
PROJECT_NAME := strategy


.PHONY: run-server
run-server:
	@cd src && python main.py --config ../configs/local.yaml

.PHONY: generate
generate:
	@python -m grpc_tools.protoc \
		-I api \
		--python_out=src/generated/grpc \
		--pyi_out=src/generated/grpc \
		--grpc_python_out=src/generated/grpc \
		api/strategy.proto
	@sed -i 's/^import strategy_pb2/from generated.grpc import strategy_pb2/' src/generated/grpc/strategy_pb2_grpc.py
	@echo "--- Proto generation done! ---"

.PHONY: test
test:
	@python -m pytest tests/producer/torch.py -v

.PHONY: freeze
freeze:
	@pip freeze > requirements.txt
	@echo "--- Freeze requirements.txt done! ---"

