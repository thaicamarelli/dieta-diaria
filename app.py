from flask import Flask,request,jsonify
from models.user import User
from database import db
from login_manager import login_manager
from controllers.user_controller import user
from controllers.meals_controller import meal

app = Flask(__name__)

app.config['SECRET_KEY'] = "BGRTH@4345454!adgar"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://maria:admin123@localhost:3306/daily-diet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(user)
app.register_blueprint(meal)

db.init_app(app)
login_manager.init_app(app)

if __name__ == '__main__':
    app.run()





