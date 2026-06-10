import mysql.connector
from PyQt5 import uic, QtCore, QtWidgets
import conexao
import os

class TelaLogin(QtWidgets.QWidget):
    login_sucesso = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        try:
            ui_path = os.path.join(os.path.dirname(__file__), "tela", "login.ui")
            print(f"Carregando UI de: {ui_path}")
            uic.loadUi(ui_path, self)
            self.setWindowTitle("Login")
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
            self.btn_login.clicked.connect(self.verificar_login)
            print("TelaLogin inicializada com sucesso")
        except Exception as e:
            print(f"Erro ao inicializar TelaLogin: {e}")
            import traceback
            traceback.print_exc()
            raise

    def verificar_login(self):
        usuario = self.txt_usuario.text()
        senha = self.txt_senha.text()

        if not usuario or not senha:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Digite usuário e senha!")
            return

        comando = "SELECT * FROM informacao WHERE usuario=%s AND senha=%s"
        dados = (usuario, senha)

        try:
            conn = conexao.conectar()
            cursor = conn.cursor()
            cursor.execute(comando, dados)
            resultado = cursor.fetchone()
        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(self, "Erro de Banco", f"Erro ao conectar: {str(e)}")
            print(f"Erro MySQL: {e}")
            return
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")
            print(f"Erro geral: {e}")
            import traceback
            traceback.print_exc()
            return
        finally:
            if 'cursor' in locals():
                try:
                    cursor.close()
                except:
                    pass
            if 'conn' in locals():
                try:
                    conn.close()
                except:
                    pass

        if resultado:
            print("Login bem-sucedido!")
            # Mostrar mensagem primeiro
            QtWidgets.QMessageBox.information(self, "Login", "Login realizado com sucesso")
            # DEPOIS emitir o sinal para navegar
            print("Emitindo sinal para abrir página principal...")
            self.login_sucesso.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Login", "Usuário ou senha incorretos")
        
