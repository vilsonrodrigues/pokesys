IMAGE ?= pokesys-app
ENV_FILE ?= .env

build:
	docker build -t $(IMAGE) .

run:
	docker run -p 8000:8000 --env-file $(ENV_FILE) $(IMAGE)	
