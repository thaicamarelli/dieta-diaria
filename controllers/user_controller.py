from flask import Blueprint,request,jsonify
import bcrypt
from database import db
from login_manager import login_manager
from models.user import User
from flask_login import login_user,current_user,logout_user,login_required

user = Blueprint('user',__name__)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@user.route('/login',methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password),str.encode(user.password)):
            
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso"})
    
    return jsonify({"message": "Credenciais inválidas"}), 400

@user.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})

@user.route('/user',methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt() ) # type: ignore
        user = User(username=username,password=hashed_password,role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario cadastrado com sucesso"})
    return jsonify({"message": "Dados invalidos"}), 400