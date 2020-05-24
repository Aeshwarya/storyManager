from app import factory
import os
import config

def run():

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    application=factory.create_app(os.path.join(BASE_DIR, 'config.py'))
    application.run(host=config.HOST , port=config.PORT)



if __name__ == "__main__":
    run()