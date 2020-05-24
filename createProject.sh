#!/bin/bash
echo "creating project:"
#echo $1
#projectname=$1
#mkdir $projectname
#cd $projectname
touch run.py
touch config.py
echo "Creating virtual environment"
python3 -m venv env
echo "Creating app"
mkdir app
touch app/__init__.py
echo "Activating virtual environment"
source env/bin/activate
echo "Installing dependencies"
env/bin/pip install flask
env/bin/pip install flask-sqlalchemy
env/bin/pip install flask-wtf



echo "Creating Models"
mkdir app/models
touch app/models/__init__.py
touch app/models/base.py

echo "Creating Controllers"
mkdir app/controllers
touch app/controllers/__init__.py

echo "Creating Services"
mkdir app/services
touch app/services/__init__.py

echo "Writing Model Base File"
modelBaseFile=app/models/base.py
cat > $modelBaseFile <<- EOM
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base(db.Model):
    __abstract__  = True
    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

EOM

echo "Writing user models"
userModelFile=app/models/users.py
cat > $userModelFile <<- EOM
from .base import db, Base

class User(Base):
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
EOM

echo "Writing Models init File"

modelsFile=app/models/__init__.py

cat > $modelsFile <<- EOM
from .base import db

def init_app(app):
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

EOM

echo "Writin UsersController"
usersControllerFile=app/controllers/usersController.py
cat > $usersControllerFile <<- EOM
from flask import Flask, make_response, Blueprint, current_app, jsonify, request
from ..services.usersService import UsersService
from ..models.users import User

UsersController = Blueprint('users_controller', __name__)
userService = UsersService(current_app)

@UsersController.route("/", methods=['GET'])
def get_users():
    users = userService.getAll()
    data = []
    for user in users:
        u = {}
        u['id']= user.id
        u['name']=user.username
        u['email']=user.email
        data.append(u)
    return make_response(jsonify(data), 200)

@UsersController.route("/", methods=['POST'])
def add_user():
    data = request.get_json()
    id = userService.addUser(data['name'], data['email'])
    return make_response(jsonify(id), 200)

EOM

echo "Writing Controllers init File"
controllersFile=app/controllers/__init__.py
cat > $controllersFile <<- EOM
from .usersController import UsersController

def init_app(app):
    app.register_blueprint(UsersController)

EOM

echo "Writing Services init File"
servicesFile=app/services/__init__.py
cat > $servicesFile <<- EOM
def init_app(app):
    pass

EOM

echo "Writing base service"
baseServiceFile=app/services/baseService.py
cat > $baseServiceFile <<- EOM
class BaseService:
    __abstract__  = True
    
    def __init__(self, app):
        self.app = app

EOM

echo "Writing user service"
userServiceFile=app/services/usersService.py
cat > $userServiceFile <<- EOM
from .baseService import BaseService
from ..models.users import User
from ..models import db

class UsersService(BaseService):
    def getAll(self):
        with self.app.app_context():
            return User.query.all()
    
    def addUser(self, name, email):
        id = -1
        with self.app.app_context():
            user = User(username=name, email=email )
            db.session.add(user)
            db.session.commit()
            id = user.id
        return id

EOM


echo "Writing project init File"
projectFile=app/__init__.py
cat > $projectFile <<- EOM
import os
from flask import Flask

def create_app(config=None):
    from . import models, controllers, services
    app = Flask(__name__)

    app.config.from_object('app.settings')

    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')
    
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    models.init_app(app)
    controllers.init_app(app)
    services.init_app(app)
    return app
EOM

touch app/settings.py

echo "Writing config file"
configFile=config.py
cat > $configFile <<- EOM
DEBUG=True
SQLALCHEMY_DATABASE_URI="sqlite:////tmp/test.db"
SQLALCHEMY_TRACK_MODIFICATIONS=False
PORT=5000
EOM

echo "Writing run File"
runFile=run.py
cat > $runFile <<- EOM
from app import create_app
import os
import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
application=create_app(os.path.join(BASE_DIR, 'config.py'))
application.run(port=config.PORT)

EOM
