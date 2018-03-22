from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = "./app/static/uploads"
app = Flask(__name__)
app.config['SECRET_KEY'] = "mykEy"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dtlbflvzbigjzg:5e04db81f5638ef194bf53d9c669cadede2ab4a70d34934376bb51610cc72f61@ec2-54-83-23-91.compute-1.amazonaws.com:5432/d7nirlmqm7p7kp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)



# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config.from_object(__name__)
filefolder = app.config['UPLOAD_FOLDER']
app.debug= True
from app import views
