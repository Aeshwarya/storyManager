import os
import logging
from flask import Flask
from . import models, controllers, services , CeleryConfig
from app.services import ResizeService

logger = logging.getLogger()

def configure_celery(app, celery):
    # Set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

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


def create_app(config=None):
    app = Flask(__name__)

    app.config['CELERY_BROKER_URL'] = CeleryConfig.CELERY_BROKER_URL
    app.config['CELERY_RESULT_BACKEND'] = CeleryConfig.CELERY_RESULT_BACKEND

    configure_celery(app, ResizeService.celery)

    models.init_app(app)
    controllers.init_app(app)
    services.init_app(app)
    return app
