VERSION := $(shell cat VERSION)
COMMIT_HASH := $(shell git rev-parse HEAD)
PROJECT_NAME := strategy


.PHONY: run-server
run-server:
	


.PHONY: freeze
freeze:
	@pip freeze > requirements.txt
	@echo "--- Freeze requirements.txt done! ---"

