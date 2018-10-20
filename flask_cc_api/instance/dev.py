SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/cc_dev'
JWT_SECRET_KEY = 'flask_cc_api'

CORS_ORIGINS = ['*']
CORS_METHODS = ['POST', 'GET', 'OPTIONS', 'DELETE', 'PATCH', 'PUT']
CORS_ALLOW_HEADERS = ['Authorization', 'Content-Type']
