#coding=utf-8
import os
import pymysql
DEBUG = True
SECRET_KEY = os.urandom(24)
#SQLALCHEMY

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'db_demo1'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)


SQLALCHEMY_TRACK_MODIFICATIONS = False
