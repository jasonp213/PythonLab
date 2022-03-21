export FLASK_APP=example

all: run

.PHONY: run
run:
	flask run

.PHONY: swagger
swagger:
	docker run --rm -d --name apispecswagger -p 8088:8080 --platform linux/amd64 -e BASE_URL=/swagger -e SWAGGER_JSON=/foo/swagger.json -v $${PWD}:/foo swaggerapi/swagger-ui

.PHONY: stop
stop:
	docker stop apispecswagger
