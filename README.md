# flask-cc-api
flask 学习 整理的 一个flask 项目框架
[学习参考](https://github.com/flaskbb/flaskbb)

## 环境搭建

### 用pyenv和virtualenv搭建多版本python环境

- 选择安装到$HOME/.pyenv目录

```
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
```

- 配置环境变量

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
```

- 添加pyenv初始化到你的shell

```
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
```

- 重新启动你的shell使更改生效。

```
exec $SHELL
source ~/.bash_profile
```

- 安装指定版本的python

```
pyenv install -v 3.6.6
```

- pyenv-virtualenv插件安装


```
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
source ~/.bash_profile
```

- 创建一个3.6.6的虚拟环境

```
pyenv virtualenv 3.6.6 env366
```

**注意**：命令中的 ‘3.6.6’ 必须是一个安装前面步骤已经安装好的python版本， 否则会出错。

- 切换和使用新的python虚拟环境

```
pyenv activate env366
```

- 如果要切换回系统环境， 运行这个命令即可

```
pyenv deactivate
```

### 安装及运行

python3.6

检查环境：

    make check 

安装相关包：

    make install

初始化数据库：

	make migrate-db

运行：

    make run

**前提**： 安装mysql 、redis ,并修改相应的配置
下载 `cc-core` 项目，与本项目放在同路径下。

---

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
