from flask import Blueprint,request,jsonify
from login_manager import login_manager
from flask_login import login_required,current_user
from models.user import User
from models.meal import Meal
from database import db

meal = Blueprint('meal',__name__)

@login_required
@meal.route('/create-meal',methods=["POST"])
def create_meal():
    data = request.json()

    name = data.get("name")
    description = data.get("description")
    datetime = data.get("datetime")
    on_diet = data.get("on_diet")

    new_meal = Meal(name=name,description=description,datetime=datetime,on_diet=on_diet)
    db.session.add(new_meal)
    db.session.commit()