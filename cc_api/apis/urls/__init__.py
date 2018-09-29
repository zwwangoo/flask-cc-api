import os
from flask import Blueprint
from .. import Api

"""
加载目录下的所有url配置文件。
url配置文件是一个python源代码文件，以url_开头，里面定义了urls（list类型）变量。
"""


def register_blueprint(app):
    for f in os.listdir(os.path.split(__file__)[0]):
        module_name, ext = os.path.splitext(f)
        if module_name.startswith('url_') and ext == '.py':
            module_blueprint = Blueprint(module_name[4:], module_name)
            module_api = Api(module_blueprint, catch_all_404s=True)
            module = __import__(__name__ + '.' + module_name, fromlist=[module_name])
            for i, url in enumerate(module.urls):
                if i % 2:
                    module_api.add_resource(module.urls[i], module.urls[i - 1])
            app.register_blueprint(module_blueprint)
