import sys
import os
from PyQt5.QtWidgets import QApplication
from login import TelaLogin
from pagina_principal import TelaPrincipal

print("=" * 70)
print("INICIANDO APLICAÇÃO - Os Bastardos")
print("=" * 70)
print(f"Python: {sys.version}")
print(f"Diretório: {os.getcwd()}")
print()

def main():
    try:
        print("[1/5] Criando QApplication...")
        app = QApplication(sys.argv)
        print("      ✓ QApplication criado com sucesso\n")

        print("[2/5] Criando TelaLogin...")
        login = TelaLogin()
        print("      ✓ TelaLogin criada com sucesso\n")
        
        print("[3/5] Definindo callback para login bem-sucedido...")
        def abrir_principal():
            print("\n[4/5] Callback executado - Abrindo TelaPrincipal...")
            try:
                login.close()
                print("      ✓ Login fechado")
                
                principal = TelaPrincipal()
                print("      ✓ TelaPrincipal criada")
                
                principal.show()
                print("      ✓ TelaPrincipal exibida\n")
                
            except Exception as e:
                print(f"      ✗ Erro ao abrir TelaPrincipal: {e}\n")
                import traceback
                traceback.print_exc()

        login.login_sucesso.connect(abrir_principal)
        print("      ✓ Callback conectado com sucesso\n")
        
        print("[5/5] Exibindo tela de login...")
        login.show()
        login.raise_()
        login.activateWindow()
        print("      ✓ Tela de login exibida\n")
        
        print("=" * 70)
        print("✓ APLICAÇÃO PRONTA")
        print("=" * 70)
        print("\nInstruções:")
        print("  1. Insira seu usuário e senha")
        print("  2. Clique em 'Login'")
        print("  3. Será redirecionado para a página principal\n")

        sys.exit(app.exec_())

    except Exception as e:
        print(f"\n✗ ERRO FATAL: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()