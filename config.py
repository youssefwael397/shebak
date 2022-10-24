# from flask_restful import fields
import pymysql
import os

# host='localhost'
# user='root'
# password= ''
# db= 'shebak'

# mysql_uri = f'mysql+pymysql://{user}:{password}@{host}:3306/{db}'


# heroku shebak-db => clear db mysql_uri
# 'mysql://b6882d20dfbdb0:553e7660@us-cdbr-east-06.cleardb.net/heroku_8f810f4920e9790?reconnect=true'

host = 'us-cdbr-east-06.cleardb.net'
user = 'b6882d20dfbdb0'
password = '553e7660'
db = 'heroku_8f810f4920e9790'


mysql_uri = f'mysql+pymysql://{user}:{password}@{host}:3306/{db}'
