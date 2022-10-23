# from flask_restful import fields
import pymysql
import os

host='localhost'
user='root'
password= ''
db= 'shebak'

mysql_uri = f'mysql+pymysql://{user}:{password}@{host}:3306/{db}'