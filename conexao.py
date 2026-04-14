import sys
import mysql.connector
# Importa classes principais do PyQt5
from PyQt5 import uic, QtWidgets

conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )