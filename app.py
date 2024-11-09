from config import Envs
from flask import Flask
from models.user import User
from database import db
from login_manager import login_manager
from controllers.user_controller import user
from controllers.meals_controller import meal

app = Flask(__name__)

app.config['SECRET_KEY'] = Envs.secret
app.config['SQLALCHEMY_DATABASE_URI'] = Envs.db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(user)
app.register_blueprint(meal)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'user.login'

if __name__ == '__main__':
    app.run()





