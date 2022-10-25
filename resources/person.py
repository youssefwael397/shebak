from flask_restful import Resource, reqparse, fields
from models.person import PersonModel
from utils.file_handler import delete_file, save_file, save_logo, delete_logo
import bcrypt
import werkzeug
import uuid
import os


class Persons(Resource):
    def get(self):
        return {"persons": [person.json() for person in PersonModel.find_all()]}


class CreatePerson(Resource):
    headers = {"Content-Type": "application/json; charset=utf-8"}

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('faculty',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('national_id',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('image',
                        type=werkzeug.datastructures.FileStorage,
                        location='files',
                        help="This field cannot be blank.",
                        required=True)

    def post(self):
        data = CreatePerson.parser.parse_args()  # person register data

        file_name = f"{uuid.uuid4().hex}.png"
        save_file(data['image'], file_name, "static/persons/image")
        data['image'] = file_name

        is_exists = PersonModel.check_if_person_exists(data)
        if is_exists:
            delete_file(file_name, "static/persons/image")
            return {"message": "This person is already exists"}, 400

        person = PersonModel(**data)
        try:
            person.save_to_db()
        except:
            return {"message": "An error occurred while creating the person."}, 500

        return {"message": "Person created successfully."}, 201


class Person(Resource):
    @classmethod
    def get(cls, person_id):
        person = PersonModel.find_by_id(person_id)
        if person:
            return person.json()
        return {"message": "Person not found."}, 404

    @classmethod
    def put(cls, person_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help="This field cannot be blank.")
        parser.add_argument('faculty',
                            type=str,
                            required=True,
                            help="This field cannot be blank.")
        parser.add_argument('national_id',
                            type=str,
                            required=True,
                            help="This field cannot be blank.")
        parser.add_argument('address',
                            type=str,
                            required=True,
                            help="This field cannot be blank.")
        parser.add_argument('image',
                            type=werkzeug.datastructures.FileStorage,
                            location='files',
                            help="This field cannot be blank.",
                            required=False)

        data = parser.parse_args()

        person = PersonModel.find_by_id(person_id)

        if not person:
            return {"message": "Person not found."}, 404

        file_name = f"{uuid.uuid4().hex}.png"

        if data['image']:

            if person.image:
                delete_file(person.image, "static/persons/image")

            save_file(data['logo'], file_name, "static/persons/image")
            person.image = file_name

        person.name = data['name']
        person.faculty = data['faculty']
        person.national_id = data['national_id']
        person.address = data['address']
        person.email = data['email']

        try:
            person.save_to_db()
        except:
            return {"message": "Duplicate data. Please change it."}, 409

        return person.json(), 200

    @classmethod
    def delete(cls, person_id):
        person = PersonModel.find_by_id(person_id)
        if not person:
            return {"message": "Person not found."}, 404
        try:
            person.delete_from_db()
            delete_file(person.logo, "static/persons/image")
        except:
            return {"message": "An error occurred while deleting the person."}, 500

        return {"message": "Person Deleted successfully."}, 201
