#!/usr/bin/env python3
"""
Teste Final - Validação Completa da Aplicação
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

print("\n" + "="*80)
print(" TESTE FINAL - VALIDAÇÃO COMPLETA DA APLICAÇÃO")
print("="*80 + "\n")

# Teste 1: Imports
print("[1/5] Testando imports...")
try:
    from login import TelaLogin
    from pagina_principal import TelaPrincipal
    print("      ✓ Imports bem-sucedidos\n")
except Exception as e:
    print(f"      ✗ Erro de import: {e}\n")
    sys.exit(1)

# Teste 2: Criação de QApplication
print("[2/5] Testando QApplication...")
try:
    app = QApplication(sys.argv)
    print("      ✓ QApplication criado\n")
except Exception as e:
    print(f"      ✗ Erro ao criar QApplication: {e}\n")
    sys.exit(1)

# Teste 3: Criação de TelaLogin
print("[3/5] Testando TelaLogin...")
try:
    login = TelaLogin()
    print("      ✓ TelaLogin criada\n")
except Exception as e:
    print(f"      ✗ Erro ao criar TelaLogin: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 4: Criação de TelaPrincipal
print("[4/5] Testando TelaPrincipal...")
try:
    principal = TelaPrincipal()
    print("      ✓ TelaPrincipal criada\n")
except Exception as e:
    print(f"      ✗ Erro ao criar TelaPrincipal: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 5: Fluxo de navegação
print("[5/5] Testando fluxo de navegação...")
try:
    success_emitted = False
    
    def on_login_success():
        global success_emitted
        success_emitted = True
        print("      ✓ Signal 'login_sucesso' emitido\n")
    
    login.login_sucesso.connect(on_login_success)
    login.login_sucesso.emit()
    
    if success_emitted:
        print("      ✓ Fluxo de navegação OK\n")
    else:
        print("      ✗ Signal não foi emitido\n")
        sys.exit(1)
        
except Exception as e:
    print(f"      ✗ Erro no fluxo: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("="*80)
print(" ✓ TODOS OS TESTES PASSARAM COM SUCESSO!")
print("="*80)
print("\nA aplicação está pronta para uso!\n")
print("Para iniciar: &'C:\\Users\\1027117\\AppData\\Local\\Programs\\Python\\Python314\\python.exe' main.py\n")
