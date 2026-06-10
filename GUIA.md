# 🎯 GUIA DE USO - Os Bastardos

## ✅ O QUE FOI CORRIGIDO

1. **Fluxo de Login → Página Principal**
   - ✓ Tela de login agora exibe corretamente
   - ✓ Mensagem "Login realizado com sucesso" aparece antes da navegação
   - ✓ Redirecionamento para página principal é suave e sem bloqueios

2. **Logs de Debug Melhorados**
   - ✓ Passo-a-passo da inicialização da aplicação
   - ✓ Mensagens claras de sucesso ou erro

3. **Widgets Verificados**
   - ✓ btn_login
   - ✓ txt_usuario
   - ✓ txt_senha

## 🚀 COMO EXECUTAR

### Opção 1: Clique em run.bat
```
Duplo clique em: run.bat
```

### Opção 2: PowerShell
```powershell
&'C:\Users\1027117\AppData\Local\Programs\Python\Python314\python.exe' main.py
```

### Opção 3: Terminal CMD
```cmd
cd C:\Users\1027117\Documents\GitHub\Os-bastardos
python main.py
```

## 📋 PASSO A PASSO

1. **Tela de Login**
   - Insira seu usuário do banco de dados
   - Insira sua senha
   - Clique no botão "Login"

2. **Validação**
   - Sistema valida as credenciais no banco de dados
   - Se correto: mensagem "Login realizado com sucesso"
   - Se incorreto: mensagem "Usuário ou senha incorretos"

3. **Navegação**
   - Após sucesso: clique OK na mensagem
   - Página Principal é aberta automaticamente
   - Login é fechado

4. **Página Principal**
   - Acesse os módulos disponíveis
   - Cadastro de Cursos
   - Relatório
   - Calendário
   - Legenda

## 🔧 ARQUIVOS PRINCIPAIS

- `main.py` - Inicialização da aplicação
- `login.py` - Tela e lógica de login
- `pagina_principal.py` - Página principal com navegação
- `conexao.py` - Conexão com banco de dados

## 💾 BANCO DE DADOS

Configuração em `conexao.py`:
```python
host = "localhost"
user = "root"
password = ""
database = "test"
```

Tabela requerida: `informacao`
- Campos: `usuario`, `senha`

## ⚠️ AVISOS

- Se houver erro de conexão com banco: verifique se MySQL está rodando
- Se as imagens não carregarem: é apenas um aviso, não afeta funcionalidade
- A aplicação requer: PyQt5 e mysql-connector-python

## ✨ TUDO FUNCIONA CORRETAMENTE!

A aplicação está pronta para uso! 🎉
