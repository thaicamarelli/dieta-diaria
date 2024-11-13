from flask import Blueprint,request,jsonify
from flask_login import login_required,current_user
from models.meal import Meal
from database import db
from datetime import datetime

meal = Blueprint('meal',__name__)

@meal.route('/meal',methods=["POST"])
@login_required
def create_meal():
    data = request.json
    user_id = current_user.id 

    name = data.get("name")
    description = data.get("description")
    date_time = data.get("datetime")
    on_diet = data.get("on_diet")

    try:
        date_time = datetime.fromisoformat(date_time)

        new_meal = Meal(name=name,description=description,datetime=date_time,on_diet=on_diet,user_id=user_id)
        db.session.add(new_meal)
        db.session.commit()

        return jsonify({"message": "Refeição cadastrada com sucesso", "Refeição": meal.to_dict()}), 201    

    except ValueError as error:
        return jsonify({"messsage": str(error)}), 400
    
    except TypeError as error:
        return jsonify({"Erro": str(error)}), 400
    
    
@meal.route('/meal/<int:id>',methods=["PUT"])
@login_required
def update_meal(id):
    try:
        meal = Meal.query.filter_by(id=id).first()

        if not meal:
            return jsonify({"message": "Refeição não encontrada"}), 404
        
        data = request.json

        if 'name' in data:
            meal.name = data['name']
        if 'description' in data:
            meal.description = data['description']
        if 'datetime' in data:
            date_time = datetime.fromisoformat(data['datetime'])
            meal.datetime = date_time
        if 'on_diet' in data:
            meal.on_diet = data['on_diet']

        db.session.commit()
        return jsonify({"message": meal.to_dict()}),200
            
    except ValueError as error:
        db.session.rollback()
        return jsonify({"messsage": str(error)}), 400
    except Exception as error:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar refeição", "erro": str(error)}),500


@meal.route('/meal/<int:id>',methods=["DELETE"])
@login_required
def delete_meal(id):
    meal = Meal.query.filter_by(id=id).first()

    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404

    try:  
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Refeição deletada com sucesso"}), 200
        
    except Exception as error:
        db.session.rollback()
        return jsonify({"message": "Erro para deletar a refeição", "erro": str(error)}), 500

@meal.route('/meal/<int:id>',methods=["GET"])
@login_required
def get_meal(id):
    meal = Meal.query.filter_by(
        id=id,
        user_id=current_user.id
        ).first()

    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404
    
    return jsonify({"message": meal.to_dict()}),200

@meal.route('/meal',methods=["GET"])
@login_required
def get_all_meals():
    meals = Meal.query.filter_by(user_id=current_user.id).all()

    if not meal:
        return jsonify({"message": "Não existem refeições cadastradas para esse usuário"}), 404
    
    meals_list = [meal.to_dict() for meal in meals]
    return jsonify({"message": meals_list}),200

