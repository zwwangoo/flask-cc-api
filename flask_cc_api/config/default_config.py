class DefaultConfig(dict):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/cc_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SUPER_ADMIN = 'admin'

    JWT_SECRET_KEY = 'cc-api'


