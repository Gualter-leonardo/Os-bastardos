import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # coloque sua senha se tiver
        database="test"
    )
    return conn

