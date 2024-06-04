all:
	docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<YourStrong@Passw0rd>" `   -p "1433:1433" --name "sql1" --hostname "sql1" -d "mcr.microsoft.com/mssql/server:2022-latest"
	sleep 10
	python -m uvicorn server:app
	python -m http.server 8080 --directory ./frontend

# docker build -t my-backend-image-name .
# docker build -t my-frontend-image-name ./frontend

