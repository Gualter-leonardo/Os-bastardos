import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # coloque sua senha se tiver
        database="seu_banco"
    )
    return conn

