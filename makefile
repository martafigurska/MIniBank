all:
	docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<YourStrong@Passw0rd>" `   -p "1433:1433" --name "sql1" --hostname "sql1" -d "mcr.microsoft.com/mssql/server:2022-latest"
	python -m uvicorn server:app
# in the frontend folder
	python /frontend -m http.server | http-server.exe

# docker build -t my-backend-image-name .
# docker build -t my-frontend-image-name ./frontend

