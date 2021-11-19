PROJECT_NAME := python_lab

ES_VERSION := 7.10.1
ES_IMAGE := elasticsearch:$(ES_VERSION)

ifeq ($(shell uname -m),arm64)
  ES_IMAGE := arm64v8/$(ES_IMAGE)
endif


start_es:
	docker run -d --rm \
	-e discovery.type=single-node \
	-p 9200:9200 \
	--name ${PROJECT_NAME}_es \
	${ES_IMAGE}

stop_es:
	docker container stop ${PROJECT_NAME}_es;