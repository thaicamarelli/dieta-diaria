from flask import Blueprint,request,jsonify
from login_manager import login_manager
from flask_login import login_required,current_user
from models.user import User
from models.meal import Meal
from database import db

meal = Blueprint('meal',__name__)

@login_required
@meal.route('/meal',methods=["POST"])
def create_meal():
    try:
        data = request.json

        name = data.get("name")
        description = data.get("description")
        datetime = data.get("datetime")
        on_diet = data.get("on_diet")

        new_meal = Meal(name=name,description=description,datetime=datetime,on_diet=on_diet)
        db.session.add(new_meal)
        db.session.commit()

        return jsonify({"message": "Refeição cadastrada com sucesso"}), 201    

    except ValueError as error:
        return jsonify({"messsage": "Erro ao cadastrar refeição valor incorreto"}), 400
    except Exception as error:
        print(error)

@login_required
@meal.route('/meal/<string:name>',methods=["PUT"])
def update_meal(name):
    try:
        meal = Meal.query.filter_by(name=name).first()

        if not meal:
            return jsonify({"message": "Refeição não encontrada"}), 404
        
        data = request.json

        if 'name' in data:
            meal.name = data['name']
        if 'description' in data:
            meal.description = data['description']
        if 'datetime' in data:
            meal.datetime = data['datetime']
        if 'on_diet' in data:
            meal.on_diet = data['on_diet']

        try:
            db.session.commit()
            return jsonify({"message": meal.to_dict()}),200
        except Exception as error:
            print(error)
    except ValueError as error:
        return jsonify({"messsage": "Erro ao atualizar refeição valor incorreto"}), 400
    except Exception as error:
        print(error)

@login_required
@meal.route('/meal/<string:name>',methods=["DELETE"])
def delete_meal(name):
    meal = Meal.query.filter_by(name=name).first()

    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404

    try:  
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Refeição deletada com sucesso"}), 200
        
    except Exception as error:
        db.session.rollback()
        return jsonify({"message": "Erro para deletar a refeição", "erro": str(error)}), 500

@login_required
@meal.route('/meal/<string:name>',methods=["GET"])
def get_meal(name):
    meal = Meal.query.filter_by(name=name).first()

    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404
    
    return jsonify({"message": meal.to_dict()}),200


# listar refeições de um usuario
