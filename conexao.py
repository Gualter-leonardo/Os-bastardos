import mysql.connector
from mysql.connector import Error

HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "sistema_cursos"


def conectar():
    """Abre uma conexão com o MySQL do XAMPP."""
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        # Evita a extensão C nativa, que pode causar access violation
        # no encerramento da conexão neste ambiente Windows/Python.
        use_pure=True,
    )


def testar_conexao():
    conn = None
    try:
        conn = conectar()
        return conn.is_connected()
    except Error:
        return False
    finally:
        if conn and conn.is_connected():
            conn.close()
