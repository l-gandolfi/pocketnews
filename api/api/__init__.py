from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.config import Config
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
ma = Marshmallow(app)
mail = Mail(app)
CORS(app, resources={r'/*': {'origins': '*'}})

from api.Access.routes import access
from api.Admin.routes import admin
from api.Settings.routes import settings
from api.Social.routes import social
from api.Home.routes import home

app.register_blueprint(access)
app.register_blueprint(admin)
app.register_blueprint(settings)
app.register_blueprint(social)
app.register_blueprint(home)