from .StoryController import UsersController

def init_app(app):
    app.register_blueprint(UsersController)

