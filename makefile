all:
	python -m uvicorn server:app

# in the frontend folder
# python -m http.server | http-server.exe