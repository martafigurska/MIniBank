all:
	docker build -t my-backend-image-name .
	docker build -t my-frontend-image-name ./frontend

# python -m uvicorn server:app
# in the frontend folder
# python -m http.server | http-server.exe
