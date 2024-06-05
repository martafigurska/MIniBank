all: help

.PHONY: help
help:
	@echo This is the help for the project
	@echo.
	@echo ------------------------------
	@echo To run the project first run:
	@echo ------------------------------
	@echo Only once:
	@echo.
	@echo   make build    - build the docker image 
	@echo   `make sure to have docker installed and running - also free port 1433
	@echo ------------------------------
	@echo Then always run in separate terminals:
	@echo.
	@echo   make backend  - run the backend server
	@echo   `make sure to have port 8000 free and the docker running
	@echo.
	@echo   make frontend - run the frontend server
	@echo   `make sure to have port 8080 free
	@echo.
	@echo   make run      - run the site
	@echo   `make sure to have chrome installed, or change the command to your browser
	@echo ------------------------------


.PHONY: build
build:
	docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<YourStrong@Passw0rd>" -p 1433:1433 --name sql1 --hostname sql1 -d mcr.microsoft.com/mssql/server:2022-latest
	del login_data.json
	
.PHONY: backend
backend:
	docker start sql1
	@echo "Waiting for the database to start"
	timeout 10
	python -m uvicorn server:app

.PHONY: frontend
frontend:
	python -m http.server 8080 --directory ./frontend

.PHONY: run
run:
	@cmd.exe /c start chrome http://127.0.0.1:8080
