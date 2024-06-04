all: help

.PHONY: run
run:
	start chrome 127.0.0.1:8080

.PHONY: help
help:
	@echo To run the project first run:
	@echo ------------------------------
	@echo Only once:
	@echo ------------------------------
	@echo make build    - build the docker image | make sure to have docker installed and free port 1433
	@echo ------------------------------
	@echo make backend  - run the backend server | make sure to have port 8000 free
	@echo make frontend - run the frontend server | make sure to have port 8080 free
	@echo make run      - run the site
	@echo ------------------------------


.PHONY: build
build:
	docker run -e ACCEPT_EULA=Y -e MSSQL_SA_PASSWORD=<YourStrong@Passw0rd> `   -p 1433:1433 --name sql1 --hostname sql1 -d mcr.microsoft.com/mssql/server:2022-latest

.PHONY: backend
backend:
	docker start sql1
	timeout 10
	python -m uvicorn server:app

.PHONY: frontend
frontend:
	python -m http.server 8080 --directory ./frontend

