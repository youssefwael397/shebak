# from flask_restful import fields
import pymysql
import os

host='localhost'
user='root'
password= ''
db= 'shebak'

mysql_uri = f'mysql+pymysql://{user}:{password}@{host}:3306/{db}'

LOGO_FOLDER = os.path.join('static/users', 'logo')


# Secretkey = 'ThisIsAReallyHardToGuessSecret!'
# resource_fields = {
#     'Country': fields.String,
#     'Name': fields.String,
#     'Surname': fields.String,
#     'Sex': fields.String,
#     'DateOfBirth': fields.Integer,
#     'Nationality': fields.String,
#     'ExpirationDate': fields.Integer,
#     'Number': fields.String,
#     'Status': fields.Boolean,
#     'Problem': fields.String
# }
# upload_path = './tempUpload'
