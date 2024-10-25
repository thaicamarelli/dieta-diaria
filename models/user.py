from database import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)
    role = db.Column(db.String(80),nullable=False, default='user')
    
    meal = relationship('Meal',back_populates='user')