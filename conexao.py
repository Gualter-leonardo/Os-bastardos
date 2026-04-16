import sys
import mysql.connector

from PyQt5 import uic, QtWidgets

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)

