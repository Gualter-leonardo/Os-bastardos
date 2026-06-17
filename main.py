import sys
import os
from PyQt5.QtWidgets import QApplication
from pagina_principal import TelaPrincipal

print("=" * 70)
print("INICIANDO APLICAÇÃO - Os Bastardos")
print("=" * 70)
print(f"Python: {sys.version}")
print(f"Diretório: {os.getcwd()}")
print()

def main():
    try:
        print("[1/3] Criando QApplication...")
        app = QApplication(sys.argv)
        print("      ✓ QApplication criado com sucesso\n")

        print("[2/3] Criando TelaPrincipal...")
        principal = TelaPrincipal()
        print("      ✓ TelaPrincipal criada com sucesso\n")

        print("[3/3] Exibindo TelaPrincipal...")
        principal.show()
        principal.raise_()
        principal.activateWindow()
        print("      ✓ TelaPrincipal exibida\n")

        print("=" * 70)
        print("✓ APLICAÇÃO PRONTA")
        print("=" * 70)

        sys.exit(app.exec_())

    except Exception as e:
        print(f"\n✗ ERRO FATAL: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()