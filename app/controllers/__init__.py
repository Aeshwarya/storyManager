from .storyController import StoryController

def init_app(app):
    app.register_blueprint(StoryController)
