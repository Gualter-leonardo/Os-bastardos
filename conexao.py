import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # coloque sua senha se tiver
        database="test"
    )
    return conn

def salvar_cadastro(nome, curso):
    print(f"[CADASTRO] {nome} - {curso}")


def gerar_relatorio():
    print("[RELATÓRIO] OK")


def configurar_calendario():
    print("[CALENDÁRIO] OK")


def carregar_legenda():
    print("[LEGENDA] OK")