PROJECT_NAME := python_lab

# since no docker image of 7.6
ES_VERSION := 7.16.3
ES_IMAGE := elasticsearch:$(ES_VERSION)

ES_HOST := localhost
ES_PORT := 9200


ifeq ($(shell uname -m),arm64)
  ES_IMAGE := arm64v8/$(ES_IMAGE)
endif

all: | check_es_fail_start load_dataset

# https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.16.3/elasticsearch-analysis-ik-7.16.3.zip

build_es:
	docker build -t my_es .

start_es:
	docker run -d --rm \
	-e discovery.type=single-node \
	-p 9200:9200 \
	--name $(PROJECT_NAME)_es \
	my_es

start_es_shell:
	docker exec -ti $(PROJECT_NAME)_es bash

check_es_fail_start:
	@curl -s http://localhost:9200/_cat/health || $(MAKE) start_es


stop_es:
	@docker container stop $(PROJECT_NAME)_es;

# setup the sample dataset
# https://www.elastic.co/guide/en/kibana/7.0/tutorial-load-dataset.html
load_dataset: bulk_shakespeare bulk_account bulk_logs

bulk_shakespeare: create_index_shakespeare shakespeare.json
	@curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/shakespeare/_bulk' --data-binary @shakespeare.json

bulk_logs: create_index_logs logs.jsonl
	@curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/_bulk' --data-binary @logs.jsonl

bulk_account: accounts.json
	@curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/bank/_bulk' --data-binary @accounts.json

create_index_shakespeare:
	@curl -X PUT "localhost:9200/shakespeare?pretty" -H 'Content-Type: application/json' -d'{"mappings": {	"properties": {	"speaker": {"type": "keyword"},	"play_name": {"type": "keyword"},	"line_id": {"type": "integer"},	"speech_number": {"type": "integer"}	}}}'

create_index_logs:
	@curl -X PUT "localhost:9200/logstash-2015.05.18?pretty" -H 'Content-Type: application/json' -d'{"mappings": {"properties": {"geo": {"properties": {"coordinates": {"type": "geo_point"}}}}}}'
	@curl -X PUT "localhost:9200/logstash-2015.05.19?pretty" -H 'Content-Type: application/json' -d'{"mappings": {"properties": {"geo": {"properties": {"coordinates": {"type": "geo_point"}}}}}}'
	@curl -X PUT "localhost:9200/logstash-2015.05.20?pretty" -H 'Content-Type: application/json' -d'{"mappings": {"properties": {"geo": {"properties": {"coordinates": {"type": "geo_point"}}}}}}'

download_dataset: shakespeare.json accounts.json logs.jsonl

shakespeare.json:
	if !([ -f $@ ]); then \
    curl -O https://download.elastic.co/demos/kibana/gettingstarted/8.x/shakespeare.json; \
	fi;

accounts.json: accounts.zip
	if !([ -f $@ ]); then \
	unzip accounts.zip; \
	fi;

accounts.zip:
	if !([ -f $@ ]); then \
	curl -O https://download.elastic.co/demos/kibana/gettingstarted/8.x/accounts.zip; \
	fi;

logs.jsonl: logs.jsonl.gz
	if !([ -f $@ ]); then \
	gunzip logs.jsonl.gz; \
	fi;

logs.jsonl.gz:
	if !([ -f $@ ]); then \
	curl -O https://download.elastic.co/demos/kibana/gettingstarted/8.x/logs.jsonl.gz; \
	fi;

.PHONY: remove_file
remove_file:
	-rm logs.jsonl.gz logs.jsonl accounts.zip accounts.json shakespeare.json

.PHONY: cleanup
cleanup: stop_es remove_file
