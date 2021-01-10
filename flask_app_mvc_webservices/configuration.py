from flask import Flask
app=Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://{}:{}@{}/{}'.format('root','root','localhost','webservice')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1238sadh1234390823kjhdJKA*(@E$^$'

db=SQLAlchemy(app)