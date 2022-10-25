from flask_restful import Resource, reqparse, fields
from models.member import MemberModel
from utils.file_handler import delete_file, save_file, save_logo, delete_logo
import bcrypt
import werkzeug
import uuid
import os
from models.user import UserModel


class Members(Resource):
    def get(self):
        return {"members": [member.json() for member in MemberModel.find_all()]}


class CreateMember(Resource):
    # headers = {"Content-Type": "application/json; charset=utf-8"}

    parser = reqparse.RequestParser()
    
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('faculty',
                        type=str,
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
        data = CreateMember.parser.parse_args()  # member register data
        if not UserModel.find_by_id(data['user_id']):
            return {"message": "This user id is invalid !"} , 404

        file_name = f"{uuid.uuid4().hex}.png"
        save_file(data['image'], file_name, "static/members/image")
        data['image'] = file_name


        is_exists = MemberModel.check_if_member_exists(data)
        if is_exists:
            delete_file(file_name, "static/members/image")
            return {"message": "This member is already exists"}, 400

        member = MemberModel(**data)
        try:
            member.save_to_db()
        except:
            return {"message": "An error occurred while creating the member."}, 500

        return {"message": "Member created successfully."}, 201


class Member(Resource):
    @classmethod
    def get(cls, member_id):
        member = MemberModel.find_by_id(member_id)
        if member:
            return member.json()
        return {"message": "Member not found."}, 404

    @classmethod
    def put(cls, member_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help="This field cannot be blank.")
        parser.add_argument('faculty',
                            type=str,
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

        # user_id before token
        parser.add_argument('user_id',
                            type=int,
                            help="This field cannot be blank.",
                            required=True)

        data = parser.parse_args()

        member = MemberModel.find_by_id(member_id)

        if not member:
            return {"message": "Member not found."}, 404

        if member.user_id != data['user_id']:
            return {"message": "Authorization Error"}, 403

        file_name = f"{uuid.uuid4().hex}.png"

        if data['image']:
            if member.image:
                delete_file(member.image, "static/members/image")

            save_file(data['image'], file_name, "static/members/image")
            member.image = file_name

        member.name = data['name']
        member.faculty = data['faculty']
        member.national_id = data['national_id']
        member.address = data['address']

        try:
            member.save_to_db()
        except:
            return {"message": "Duplicate data. Please change it."}, 409

        return member.json(), 200

    @classmethod
    def delete(cls, member_id):
        member = MemberModel.find_by_id(member_id)
        if not member:
            return {"message": "Member not found."}, 404
        try:
            member.delete_from_db()
            delete_file(member.logo, "static/members/image")
        except:
            return {"message": "An error occurred while deleting the member."}, 500

        return {"message": "Member Deleted successfully."}, 201


class MemberUser(Resource):
    @classmethod
    def get(cls, user_id):
        return {"members": [member.json() for member in MemberModel.find_by_user_id(user_id)]}
