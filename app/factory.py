import os
import logging
from flask import Flask
from . import models, controllers, services , CeleryConfig, dm_model
from app.services import resizeService
from . import settings

logger = logging.getLogger()

def configure_celery(app, celery):
    # Set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    # Subclass task base for app context
    task_base = celery.Task

    class AppContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery.Task = AppContextTask

    # Run finalize to process decorated tasks
    celery.finalize()

# def create_worker():
#     app = Flask(__name__)

#     print(CeleryConfig.CELERY_BROKER_URL)
#     print(CeleryConfig.CELERY_RESULT_BACKEND)
#     app.config['CELERY_BROKER_URL'] = CeleryConfig.CELERY_BROKER_URL
#     app.config['CELERY_RESULT_BACKEND'] = CeleryConfig.CELERY_RESULT_BACKEND

#     configure_celery(app, ResizeService.celery)
#     return ResizeService.celery


def create_app(mode='app'):
    app = Flask(__name__)

    app.config['CELERY_BROKER_URL'] = CeleryConfig.CELERY_BROKER_URL
    app.config['CELERY_RESULT_BACKEND'] = CeleryConfig.CELERY_RESULT_BACKEND

    if (mode == 'test'):
        app.config['task_always_eager'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['MAX_CONTENT_LENGTH']=settings.MAX_CONTENT_LENGTH
    app.config['ALLOWED_EXTENSIONS']=settings.ALLOWED_EXTENSIONS

    configure_celery(app, resizeService.celery)

    dm_model.init_app(app)
    controllers.init_app(app)
    services.init_app(app)

    
    if mode == 'worker':
        return resizeService.celery

    return app
