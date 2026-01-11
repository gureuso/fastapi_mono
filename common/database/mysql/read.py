# -*- coding: utf-8 -*-
import databases
import pymysql

from config import Config

pymysql.install_as_MySQLdb()

DATABASE_URL = f'''mysql://{Config.DB_USER_NAME}:{Config.DB_USER_PASSWD}@{Config.DB_HOST}/{Config.DB_NAME}'''
read_database = databases.Database(DATABASE_URL)
