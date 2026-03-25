import mysql.connector

def get_connection():
    return mysql.connector.connect(

import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=os.environ.get("MYSQLPORT")
    )
        user="root",
        password="12345678",
        database="vocab_app"
    )
