# Elasticsearch DSL

Version: 7.6.0
Document: https://elasticsearch-dsl.readthedocs.io/en/latest/
Repository: https://github.com/elastic/elasticsearch-dsl-py

download office sample data: https://www.elastic.co/guide/en/kibana/7.6/tutorial-build-dashboard.html#load-dataset

## elasticsearch prepare

- install `docker` `make`
```
make
```

## TODO

- using sample create APIs

- [x] Write `makefile` for setup env convenient
- [x] Different of the `Document._index` and `Document.index`
Since IDE warning the field start of underline, the [document is using _index](https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html?highlight=template#indextemplate)

## Note:

The API main component
- Index
- Document
- Search

## Analyzer IK

這裡安裝了IK analyzer，因為一些技術性問題沒有直接使用 elastic-plugin install


## Others:

### mapping types
這裡在找資料的時候混用到
[Kibana 7.0](https://www.elastic.co/guide/en/kibana/7.0/tutorial-load-dataset.html)
版本的 sample data，當中試著使用 elasticsearch-dsl 建立 document 發現到一個地方是與前面 7.6 版本 sample data 有差異的地方，
在
- 7.0
`POST bank/account/_bulk`
- 7.6
`POST bank/_bulk`

這是源至於一個 deprecated 的設計 mapping types
>`_type` field
>Deprecated in 6.0.0.
See [Removal of mapping types](https://www.elastic.co/guide/en/elasticsearch/reference/current/removal-of-types.html)


reference:
- [iThome Elastic Stack第十四重](https://ithelp.ithome.com.tw/articles/10246071)
