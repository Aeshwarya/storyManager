import  os

MAX_HEIGHT = 1200
MAX_WIDTH = 600
VIDEO_QUALITY = 480
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FILE_STORE_PATH =  BASE_DIR+'/store/'
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAX_CONTENT_LENGTH=50*1024*1024 #50MB
ALLOWED_EXTENSIONS=['jpg', 'jpeg', 'mp4']

