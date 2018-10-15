"""
Load the urls configuration in the current directory.
Routing file naming must end with '_urls.py', e.g. auth_urls.py.
There must be an array of urls in the routing file,
and the route appears in pairs with the processing view.
e.g.
urls = [
    '/auth/login', LoginHandler
]
"""

import os
import importlib
import traceback
from flask import Blueprint
from .. import Api


def register_blueprint(app):
    for f in os.listdir(os.path.split(__file__)[0]):
        module_name, ext = os.path.splitext(f)
        if module_name.endswith('_urls') and ext == '.py':

            module_blueprint = Blueprint(module_name[:-5], module_name)
            module_api = Api(module_blueprint, catch_all_404s=True)

            try:
                module = importlib.import_module('.' + module_name, __package__)
            except Exception as err:
                print(traceback.format_exc())
                os._exit(0)

            for i, url in enumerate(module.urls):
                if i % 2:
                    module_api.add_resource(module.urls[i], module.urls[i - 1])
            app.register_blueprint(module_blueprint)
