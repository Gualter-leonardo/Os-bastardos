import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from login import TelaLogin
from pagina_principal import TelaPrincipal

def simular_login():
    """Simula um login bem-sucedido e testa a navegação"""
    print("=" * 50)
    print("TESTE DE NAVEGAÇÃO LOGIN → PRINCIPAL")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    print("\n1. Criando TelaLogin...")
    login = TelaLogin()
    
    def abrir_principal():
        print("\n3. Signal 'login_sucesso' recebido!")
        print("   Fechando login...")
        login.close()
        
        try:
            print("   Criando TelaPrincipal...")
            principal = TelaPrincipal()
            print("   Exibindo TelaPrincipal...")
            principal.show()
            print("\n✓ SUCESSO: Navegação completada com sucesso!")
        except Exception as e:
            print(f"\n✗ ERRO ao abrir principal: {e}")
            import traceback
            traceback.print_exc()
    
    # Conectar o sinal
    print("2. Conectando signal 'login_sucesso'...")
    login.login_sucesso.connect(abrir_principal)
    
    print("   Signal conectado com sucesso!")
    print("\n4. Emitindo signal 'login_sucesso' em 1 segundo...")
    
    # Emitir o sinal após 1 segundo
    QtCore.QTimer.singleShot(1000, lambda: (
        print("   → Emitindo signal..."),
        login.login_sucesso.emit(),
        QtCore.QTimer.singleShot(2000, app.quit)  # Fechar app após 2 segundos
    ))
    
    login.show()
    print("\n5. Iniciando aplicação...\n")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    simular_login()
