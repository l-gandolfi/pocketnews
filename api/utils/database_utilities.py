from psycopg2 import connect, extensions, sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from api import db

def create_database():
    # local use: your username & psw
    con = connect(dbname='news_db', user='pgadmin', host='db', password='pgadmin')
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
    try:
    	cursor.execute('CREATE DATABASE news_db')
    except Exception:
        pass
    cursor.close()
    con.close()

def create_table():
    print("Creating tables...")
    db.create_all()
