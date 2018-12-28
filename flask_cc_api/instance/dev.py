SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/flask-cc-api-dev.db'
JWT_SECRET_KEY = 'flask_cc_api'

CORS_ORIGINS = ['*']
CORS_METHODS = ['POST', 'GET', 'OPTIONS', 'DELETE', 'PATCH', 'PUT']
CORS_ALLOW_HEADERS = ['Authorization', 'Content-Type']
