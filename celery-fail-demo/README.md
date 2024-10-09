# 古蹟維護的版本上限（WIP）

最近看 [`pyproject.toml` 是如何配置](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)，
原本對當中說不建議為依賴設置版本上限感到奇怪，亦賴關係會像是這樣子
```toml
[project]
name = "your-project"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
]
```
實際開發則是常常會發生如果不設定上限，那些有一點歷史的專案就會遇到各種依賴問題。

## TL;DR

分成 Application 和 Package 開發兩個場景
- Package 開發遵照建議不設定上限
- Application 開發使用 lockfile
    ```shell
    # Simple lockfile without poetry, pdm or uv.
    pip freeze > requirements-lock.txt
    pip install --no-deps -r requirements-lock.txt
    ```

## pinning python version

裡面這篇[discussion](https://iscinumpy.dev/post/bound-version-constraints/#pinning-the-python-version-is-special)
則是稍微解開一些疑惑，這建議對象是 package 開發者，
在配置上限版本的情況下，對於引用了這份 package 的專案會造成更大的麻煩，
根據[海侖定律](https://www.hyrumslaw.com/)，不管做出什麼修改都有可能是 breaking change，

## 之前遇到的例子

首先設定 Python(3.7.12) 虛擬環境
```shell
python -m venv venv
source venv/bin/activate

pip install 'celery[redis]==4.3.0'
```
安裝時就會看到第一個 ERROR `amqp 2.6.1` 需要 `vine<5.0.0a1` 但是安裝了 `vine 5.1.0` 但整體還是安裝成功(`pip install`失敗應該會整個退回，不知道為什麼邊沒有退回)
```shell
ERROR: amqp 2.6.1 has requirement vine<5.0.0a1,>=1.1.3, but you'll have vine 5.1.0 which is incompatible.
Installing collected packages: billiard, vine, typing-extensions, zipp, importlib-metadata, amqp, kombu, pytz, async-timeout, redis, celery
Successfully installed amqp-2.6.1 async-timeout-4.0.3 billiard-3.6.4.0 celery-4.3.0 importlib-metadata-6.7.0 kombu-4.6.11 pytz-2024.2 redis-5.0.8 typing-extensions-4.7.1 vine-5.1.0 zipp-3.15.0
```
第一次執行 worker 發生 ModuleNotFoundError
```shell
$ celery -A celery_app worker --loglevel=info

Traceback ...
ModuleNotFoundError: No module named 'vine.five'
```
Fine，是 `vine` 版本問題，手動執行安裝 `pip install 'vine<5.0.0a1'`，然後再次實行 `celery worker` 還是發生錯誤
```shell
$ celery -A celery_app worker --loglevel=info

Traceback (most recent call last):
...
    for ep in importlib_metadata.entry_points().get(namespace, [])
AttributeError: 'EntryPoints' object has no attribute 'get'
```
這次是`importlib-metadata`發生問題，可以執行`pip install 'importlib-metadata==4.13.0'`，實行 `celcey worker`
```shell
$ celery -A celery_app worker --loglevel=info
...
[2024-10-01 14:29:24,500: ERROR/MainProcess] consumer: Cannot connect to redis://localhost:6379/0: Error 61 connecting to localhost:6379. Connection refused..
Trying again in 2.00 seconds...
```
Redis服務不存在，`docker run --rm --name redis -p 6379:6379 -d redis`，再次執行，終於成功啟動 celery worker !
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
最後，如果一開始`Python==3.8`到`pip install 'celery[redis]==4.3.0'`就可以收工，不過身為維護員只能選擇`3.7`
