from app import factory

celery = factory.create_app('worker')
