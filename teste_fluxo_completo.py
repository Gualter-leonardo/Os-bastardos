#!/usr/bin/env python3
"""
Teste completo do fluxo: Login → Mensagem de Sucesso → Página Principal
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from login import TelaLogin
from pagina_principal import TelaPrincipal

def teste_completo():
    print("\n" + "="*70)
    print("TESTE COMPLETO: LOGIN → MENSAGEM → PÁGINA PRINCIPAL")
    print("="*70 + "\n")
    
    app = QApplication(sys.argv)
    
    # 1. Criar login
    print("[1/4] Criando tela de login...")
    login = TelaLogin()
    print("      ✓ TelaLogin criada\n")
    
    # 2. Conectar signal
    print("[2/4] Conectando signal 'login_sucesso'...")
    
    def abrir_principal():
        print("\n[4/4] Signal recebido - Abrindo página principal...")
        login.close()
        try:
            principal = TelaPrincipal()
            principal.show()
            print("      ✓ Página Principal exibida\n")
            print("="*70)
            print("✓ TESTE CONCLUÍDO COM SUCESSO!")
            print("="*70 + "\n")
        except Exception as e:
            print(f"✗ Erro: {e}")
            import traceback
            traceback.print_exc()
    
    login.login_sucesso.connect(abrir_principal)
    print("      ✓ Signal conectado\n")
    
    # 3. Simular login
    print("[3/4] Simulando login em 1 segundo...")
    print("      (A mensagem de sucesso será exibida)\n")
    
    def simular_login():
        print("→ Emitindo sinal de login bem-sucedido...")
        login.login_sucesso.emit()
    
    QtCore.QTimer.singleShot(1000, simular_login)
    QtCore.QTimer.singleShot(4000, app.quit)  # Sair após 4 segundos
    
    login.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    teste_completo()
