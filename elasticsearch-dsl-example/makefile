PROJECT_NAME := python_lab

ES_VERSION := 7.10.1
ES_IMAGE := elasticsearch:$(ES_VERSION)
KIBANA_IMAGE := kibana:7.13.1

ifeq ($(shell uname -m),arm64)
  ES_IMAGE := arm64v8/$(ES_IMAGE)
endif

all: check_es_fail_start
	$(MAKE) load_sample_data

start_es:
	docker run -d --rm \
	-e discovery.type=single-node \
	-p 9200:9200 \
	--name $(PROJECT_NAME)_es \
	$(ES_IMAGE); \
	sleep 5

check_es_fail_start:
	@curl -s http://localhost:9200/_cat/health || $(MAKE) start_es


stop_es:
	@docker container stop $(PROJECT_NAME)_es;

# setup the sample dataset
# https://www.elastic.co/guide/en/kibana/7.0/tutorial-load-dataset.html
load_sample_data: load_shakespeare load_account load_logs

load_shakespeare: mapping_shakespeare shakespeare.json
	@curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/shakespeare/_bulk?pretty' --data-binary @shakespeare.json

load_logs: mapping_logs logs.jsonl
	@curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/_bulk?pretty' --data-binary @logs.jsonl

load_account: accounts.json
	@curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/bank/account/_bulk?pretty' --data-binary @accounts.json

mapping_shakespeare:
	@curl -X PUT "localhost:9200/shakespeare?pretty" -H 'Content-Type: application/json' -d'{"mappings": {	"properties": {	"speaker": {"type": "keyword"},	"play_name": {"type": "keyword"},	"line_id": {"type": "integer"},	"speech_number": {"type": "integer"}	}}}'

mapping_logs:
	@curl -X PUT "localhost:9200/logstash-2015.05.18?pretty" -H 'Content-Type: application/json' -d'{"mappings": {"properties": {"geo": {"properties": {"coordinates": {"type": "geo_point"}}}}}}'
	@curl -X PUT "localhost:9200/logstash-2015.05.19?pretty" -H 'Content-Type: application/json' -d'{"mappings": {"properties": {"geo": {"properties": {"coordinates": {"type": "geo_point"}}}}}}'
	@curl -X PUT "localhost:9200/logstash-2015.05.20?pretty" -H 'Content-Type: application/json' -d'{"mappings": {"properties": {"geo": {"properties": {"coordinates": {"type": "geo_point"}}}}}}'

dataset: shakespeare.json accounts.json logs.jsonl

shakespeare.json:
	if !([ -f $@ ]); then \
	curl -O https://download.elastic.co/demos/kibana/gettingstarted/7.x/shakespeare.json; \
	fi;

accounts.json: accounts.zip
	if !([ -f $@ ]); then \
	unzip accounts.zip; \
	fi;

accounts.zip:
	if !([ -f $@ ]); then \
	curl -O https://download.elastic.co/demos/kibana/gettingstarted/7.x/accounts.zip; \
	fi;

logs.jsonl: logs.jsonl.gz
	if !([ -f $@ ]); then \
	gunzip logs.jsonl.gz; \
	fi;

logs.jsonl.gz:
	if !([ -f $@ ]); then \
	curl -O https://download.elastic.co/demos/kibana/gettingstarted/7.x/logs.jsonl.gz; \
	fi;

.PHONY: cleanup remove_file

remove_file:
	-rm logs.jsonl.gz logs.jsonl accounts.zip accounts.json shakespeare.json

cleanup: stop_es remove_file
