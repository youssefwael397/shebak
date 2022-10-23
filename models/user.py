from enum import unique
from db import db


class UserModel(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer(), primary_key=True)
    company_name = db.Column(db.String(50), unique=True, nullable=False)
    logo = db.Column(db.String(255), unique=True, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __init__(self, company_name, email, password, logo):
        self.company_name = company_name
        self.password = password
        self.email = email
        self.logo = logo
    
    def json(self):
        return {
            'id':self.id,
            'company_name': self.company_name,
            'email': self.email,
            'password': self.password,
            }
    
    @classmethod    
    def find_by_company_name(cls, company_name):
        return cls.query.filter_by(company_name=company_name).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def check_if_user_exists(self, user):
        if self.find_by_company_name(user['company_name']) or self.find_by_email(user['email']):
            return True
        return False
    
    @classmethod    
    def find_by_id(cls, _id):
       return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        # SQL_ALCHEMY automatically checks if the data is changed, so takes care of both insert
        # and update
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

