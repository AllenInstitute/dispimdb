import os

basedir = os.path.abspath(os.path.dirname(__file__))

ENVIRON_DATABASE_URI = os.getenv("DISPIMDB_MONGO_URI")
ENVIRON_DATABASE_NAME = os.getenv("DISPIMDB_DATABASE_NAME")


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'dev'
    DATABASE_URI = ENVIRON_DATABASE_URI or 'mongodb://localhost:27017'
    DATABASE_NAME = ENVIRON_DATABASE_NAME or 'dispimdb'
    #IMAGE_UPLOAD_PATH = '/home/samk/acworkflow_storage/images'
    IMAGE_UPLOAD_PATH = '/images'
    ALLOWED_IMAGE_EXT = {'png', 'jpg', 'jpeg', 'gif'}

    CELERY_BROKER_URL = 'amqp://'
    CELERY_RESULT_BACKEND = 'rpc://'
    FLOWER_URL = '/flower'

class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_NAME = 'dispimdb_test'
