from db import db
import os


class PersonModel(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    faculty = db.Column(db.String(255), nullable=False)
    national_id = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id'), nullable=False)

    def __init__(self, name, faculty, national_id, address, image, user_id):
        self.name = name
        self.faculty = faculty
        self.national_id = national_id
        self.address = address
        self.image = image
        self.user_id = user_id

    def json(self):
        return {
            'id': self.name,
            'faculty': self.faculty,
            'national_id': self.national_id,
            'address': self.address,
            'image': self.image,
            'user_id': self.user_id
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_national_id(cls, national_id):
        return cls.query.filter_by(national_id=national_id).first()

    @classmethod
    def check_if_user_exists(self, user):
        if self.find_by_name(user['name']) or self.find_by_email(user['national_id']):
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
