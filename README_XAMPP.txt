1. Abra o XAMPP.
2. Inicie o MySQL (Apache nao e necessario para o programa Python).
3. Abra o phpMyAdmin.
4. Importe o arquivo banco_sistema_cursos.sql.
5. Instale as dependencias:
   pip install PyQt5 mysql-connector-python
6. Execute main.py.

Login inicial criado no banco:
Usuario: admin
Senha: 1234

O arquivo principal.ui original NAO foi alterado.
A correcao do banner e feita somente em tempo de execucao, porque a UI original
usa o recurso Qt :/logo/banner_senac_v2.png sem um arquivo .qrc carregado.
O banner utilizado esta em tela/banner_senac_v2.png.

As telas principais usam a mesma conexao com o banco sistema_cursos:
- Login -> informacao
- Cadastro de curso -> cursos2
- Cadastro de UC -> grade
- Legendas/eventos -> eventos
- Relatorio -> cursos2
- Calendario -> eventos

Agenda de UCs no calendario:
- Cadastre o curso com a data inicial no formato DD/MM/AAAA.
- No cadastro da UC, informe no campo CURSO o nome exato do curso.
- As UCs sao organizadas pela POSICAO e coloridas de segunda a sexta, considerando 3 horas por dia.
- O programa adiciona automaticamente a coluna de vinculo curso/UC em bancos antigos.
