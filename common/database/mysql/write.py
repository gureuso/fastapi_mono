# -*- coding: utf-8 -*-
import databases
import pymysql
import sqlalchemy

from config import Config

pymysql.install_as_MySQLdb()

DATABASE_URL = f'''mysql://{Config.DB_USER_NAME}:{Config.DB_USER_PASSWD}@{Config.DB_HOST}/{Config.DB_NAME}'''
write_database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
user_table = sqlalchemy.Table(
    'User',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column('num', sqlalchemy.String(10), unique=True),
    sqlalchemy.Column('email', sqlalchemy.String(255), unique=True),
    sqlalchemy.Column('provider', sqlalchemy.String(40)),
    sqlalchemy.Column('created_at', sqlalchemy.TIMESTAMP),
)