# Why we need upper cap on everything (暫)

這篇文章[blog](https://iscinumpy.dev/post/bound-version-constraints/#pinning-the-python-version-is-special)說我們不需要為`pyproject.toml`設置版本上限，
但實際開發則是常常會發生如果不設定上限，
那些開源庫就會教會你什麼是 breaking change

## TL;DR

內文有提到只用 `pip` 的簡易 lockfile 作法
```shell
pip freeze > requirements-lock.txt
pip install --no-deps -r requirements-lock.txt
```

## 這裡有一個小小的反例

首先設定 Python 虛擬環境
```shell
python -V  # Python 3.7.12

python -m venv venv
source venv/bin/activate

pip install 'celery[redis]==4.3.0'
```

安裝時就會看到第一個 ERROR `amqp 2.6.1` 需要 `vine<5.0.0a1` 但是安裝了 `vine 5.1.0` 但還是安裝成功

```shell
ERROR: amqp 2.6.1 has requirement vine<5.0.0a1,>=1.1.3, but you'll have vine 5.1.0 which is incompatible.
Installing collected packages: billiard, vine, typing-extensions, zipp, importlib-metadata, amqp, kombu, pytz, async-timeout, redis, celery
Successfully installed amqp-2.6.1 async-timeout-4.0.3 billiard-3.6.4.0 celery-4.3.0 importlib-metadata-6.7.0 kombu-4.6.11 pytz-2024.2 redis-5.0.8 typing-extensions-4.7.1 vine-5.1.0 zipp-3.15.0
```

第一次執行 worker 發生 ModuleNotFoundError

```shell
celery -A celery_app worker --loglevel=info

Traceback ...
ModuleNotFoundError: No module named 'vine.five'
```

OK 真的是 `vine` 版本問題，手動執行安裝 `pip install 'vine<5.0.0a1'`，然後再次實行 `celery worker` 還是發生錯誤

```shell
celery -A celery_app worker --loglevel=info

Traceback (most recent call last):
...
    for ep in importlib_metadata.entry_points().get(namespace, [])
AttributeError: 'EntryPoints' object has no attribute 'get'
```

經過一番搜尋 `pip install 'importlib-metadata==4.13.0'`，實行 `celcey worker`

```shell
celery -A celery_app worker --loglevel=info

...
[2024-10-01 14:29:24,500: ERROR/MainProcess] consumer: Cannot connect to redis://localhost:6379/0: Error 61 connecting to localhost:6379. Connection refused..
Trying again in 2.00 seconds...
```

喔，這次因為缺少 redis `docker run --rm --name redis -p 6379:6379 -d redis`，再次執行，終於成功啟動 celery woker !

```shell
 --------------
---- **** ----- 
--- * ***  * -- Darwin-23.4.0-arm64-arm-64bit 2024-10-01 14:30:48
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x1060f71c8
- ** ---------- .> transport:   redis://localhost:6379/0
- ** ---------- .> results:     redis://localhost:6379/0
- *** --- * --- .> concurrency: 8 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
```

執行 `python main.py`，完成撒花
```
Task ID: bb932e99-667b-4cea-b562-6e9ea2ea3f78
Task Status: PENDING
Task Result: 10
```

最後，如果一開始使用 `Python 3.8` 則不會有上述問題。
