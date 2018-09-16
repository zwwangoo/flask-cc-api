# cc-api
flask 学习 整理的 一个flask 项目框架
[学习参考](https://github.com/flaskbb/flaskbb)

python3.6

检查环境：

    make check 

安装相关包：

    make install
运行：

    make run

## 关于celery

启动worker：

    celery -A celery_worker.celery --loglevel=info worker

启动 Celery Beat 进程，定时将任务发送到 Broker

    celery beat -A celery_worker.celery

异步执行：

```
# api.py

from cc_api.proj.tasks import add

    ……
    add.apply_async((2, 2), countdown=10)
    ……


# proj.tasks.py
from cc_api.extensions import celery

@celery.task(bind=True)
def add(self, a, b):
    c = a + b
    print('celery tasks……')
    return a + b

```
