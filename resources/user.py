from flask_restful import Resource, reqparse, fields
from numpy import empty
from models.user import UserModel


class Users(Resource):
    def get(self):
        return {"users": [user.json() for user in UserModel.find_all()]}


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('company_name',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('logo',
                        type=str,
                        help="This field cannot be blank.")
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()
        print(data)
        
        is_exists = UserModel.check_if_user_exists(data)
        if is_exists:
            return {"message": "A user with that company_name already exists"}, 400
        # if not => create new user

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        pass

    @classmethod
    def delete(cls, user_id):
        pass


class CreateStaticUser(Resource):

    def get(self):
        data = {
            "company_name": "youssefwael",
            'logo': "",
            'email': 'youssefwael397@gmail.com',
            "password": "12345678"
        }
        print(data)
        # check_if_user_exists 
        is_exists = UserModel.check_if_user_exists(data)
        if is_exists:
            return {"message": "A user with that company_name already exists"}, 400
        # if not => create new user
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
