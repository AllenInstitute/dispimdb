import os

from flask import Flask
from celery import Celery
from app.config import Config, DevelopmentConfig

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)

    celery.conf.update(app.config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from . import base
    app.register_blueprint(base.bp)

    from . import api
    app.register_blueprint(api.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import tracker
    app.register_blueprint(tracker.bp)

    from . import tasks
    app.register_blueprint(tasks.bp)

    from . import viz
    app.register_blueprint(viz.bp)

    return app