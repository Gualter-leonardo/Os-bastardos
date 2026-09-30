import os
from datetime import date, datetime, timedelta
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import mysql.connector
import conexao
from ajuste_principal import adaptar_tela_principal


class TelaPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        caminho = os.path.join(
            os.path.dirname(__file__), "tela", "principal.ui"
        )

        # A sua UI original usa a imagem do banner como recurso Qt (: /logo/...).
        # Como o projeto não possui um .qrc compilado, o Qt procura esse recurso
        # e gera "Could not create pixmap from :\logo\banner_senac_v2.png".
        # Mantemos o .ui original intacto e corrigimos somente a carga em tempo de execução.
        with open(caminho, "r", encoding="utf-8") as arquivo:
            ui_xml = arquivo.read()

        banner = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "tela", "banner_senac_v2.png")
        ).replace("\\", "/")

        ui_xml = ui_xml.replace(
            ":/logo/banner_senac_v2.png", banner
        )
        ui_xml = ui_xml.replace(
            ":/banner_senac_v2.png", banner
        )
        ui_xml = ui_xml.replace(
            "../Icon, itens e etc/banner_senac_v2.png", banner
        )
        ui_xml = ui_xml.replace(
            "<pixmap>banner_senac_v2.png</pixmap>",
            f"<pixmap>{banner}</pixmap>",
        )

        # Resolve também os ícones que o Designer gravou como recursos Qt.
        pasta_tela = os.path.join(os.path.dirname(__file__), "tela")
        imagens = {
            ":/icon.png/icons8-losango-32.png.png": "icons8-losango-32.png.png",
            ":/icons8-losango-32.png.png": "icons8-losango-32.png.png",
            ":/icons8-circle-50 1.png": "icons8-circle-50 1.png",
            ":/icon.png/icons8-fluxograma-32.png": "icons8-fluxograma-32.png",
            ":/icons8-fluxograma-32.png": "icons8-fluxograma-32.png",
            ":/icon.png/icons8-forma-de-papagaio-32.png": "icons8-pol#U00edgono-32.png.png",
            ":/icon.png/icons8-communication-32.png": "icons8-communication-32.png",
            ":/icons8-communication-32.png": "icons8-communication-32.png",
            ":/icons8-triângulo-50.png": "icons8-tri#U00e2ngulo-50.png",
            ":/icons8-management-50.png": "icons8-management-50.png",
            ":/icon.png/icons8-quadrado-arredondado-32.png.png": "icons8-quadrado-arredondado-32.png.png",
            ":/icons8-quadrado-arredondado-32.png.png": "icons8-quadrado-arredondado-32.png.png",
            ":/icon.png/icons8-graph-32.png.png": "icons8-graph-32.png.png",
            ":/icons8-graph-32.png.png": "icons8-graph-32.png.png",
        }
        for referencia, nome_arquivo in imagens.items():
            arquivo_imagem = os.path.abspath(
                os.path.join(pasta_tela, nome_arquivo)
            ).replace("\\", "/")
            if os.path.isfile(arquivo_imagem):
                ui_xml = ui_xml.replace(referencia, arquivo_imagem)
        from io import StringIO
        uic.loadUi(StringIO(ui_xml), self)
        adaptar_tela_principal(self)

        self._configurar_telas()
        self._conectar_botoes()
        self._configurar_calendarios()
        self._garantir_vinculo_uc_curso()

        # Carrega os dados assim que a tela abre.
        self.carregar_relatorio()
        self.carregar_calendario()

    def closeEvent(self, event):
        # O app não encerra ao fechar o login; encerra quando a principal fecha.
        event.accept()
        QtWidgets.QApplication.instance().quit()

    def _configurar_telas(self):
        self.TAB3.setCurrentIndex(0)
        self.txt_inicio.setPlaceholderText("DD/MM/AAAA")
        self.txt_curso.setPlaceholderText("Nome exato do curso cadastrado")
        self.txt_quantidade_uc.setPlaceholderText("Quantidade de UCs")
        self.txt_horas_uc.setPlaceholderText("Horas da UC")
        self.txt_posicao.setPlaceholderText("Posição")

    def _conectar_botoes(self):
        self.btn_cadastrar.clicked.connect(self.salvar_curso)
        self.btn_uc_cadastrar.clicked.connect(self.salvar_uc)
        self.btn_legenda.clicked.connect(self.salvar_legendas)
        self.btn_carregar.clicked.connect(self.carregar_relatorio)

        # Ao trocar de aba, atualiza os dados que dependem do banco.
        self.TAB3.currentChanged.connect(self._aba_alterada)

    def _aba_alterada(self, indice):
        if indice == 2:
            self.carregar_relatorio()
        elif indice == 3:
            self.carregar_calendario()

    def _configurar_calendarios(self):
        # Todos os calendários existentes na sua UI passam a usar os eventos
        # gravados no banco para destacar os dias com evento.
        for calendario in self.findChildren(QtWidgets.QCalendarWidget):
            calendario.selectionChanged.connect(self._calendario_selecionado)

    def _garantir_vinculo_uc_curso(self):
        """Atualiza instalações antigas, que ainda não tinham curso_id na grade."""
        conn = None
        cursor = None
        try:
            conn = self._abrir_conexao()
            cursor = conn.cursor()
            cursor.execute("SHOW COLUMNS FROM grade LIKE 'id_curso'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE grade ADD COLUMN id_curso INT NULL")
                conn.commit()
        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(
                self, "Erro ao preparar o banco", str(e)
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def _ler_data_inicio(valor):
        valor = valor.strip()
        for formato in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(valor, formato).date()
            except ValueError:
                pass
        raise ValueError("Informe a data inicial no formato DD/MM/AAAA.")

    @staticmethod
    def _cor_da_uc(id_uc):
        matiz = (int(id_uc) * 137) % 360
        return QtGui.QColor.fromHsv(matiz, 95, 245)

    def _mes_do_calendario(self, calendario, fallback):
        meses = {
            "JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4,
            "MAI": 5, "JUN": 6, "JUL": 7, "AGO": 8,
            "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12,
        }
        pagina = calendario.parentWidget()
        for abas in self.findChildren(QtWidgets.QTabWidget):
            indice = abas.indexOf(pagina)
            if indice >= 0:
                titulo = abas.tabText(indice).strip().upper()[:3]
                return meses.get(titulo, fallback)
        return fallback

    def _preencher_calendario_com_ucs(self, cursor):
        cursor.execute(
            """
            SELECT c.id_curso, c.curso, c.inicio,
                   g.id_uc, g.nome_uc, g.horas_uc
            FROM cursos2 c
            JOIN grade g ON g.id_curso = c.id_curso
            ORDER BY c.id_curso, g.posicao, g.id_uc
            """
        )
        linhas = cursor.fetchall()

        cursos = {}
        for id_curso, nome_curso, inicio, id_uc, nome_uc, horas_uc in linhas:
            if id_curso not in cursos:
                try:
                    data_inicio = self._ler_data_inicio(str(inicio or ""))
                except ValueError:
                    continue
                cursos[id_curso] = {
                    "nome": nome_curso,
                    "data": data_inicio,
                    "ucs": [],
                }
            cursos[id_curso]["ucs"].append((id_uc, nome_uc, int(horas_uc)))

        calendarios = self.findChildren(QtWidgets.QCalendarWidget)
        for data_antiga in getattr(self, "_ucs_por_data", {}):
            dia_antigo = QtCore.QDate.fromString(data_antiga, "yyyy-MM-dd")
            for calendario in calendarios:
                calendario.setDateTextFormat(dia_antigo, QtGui.QTextCharFormat())

        self._ucs_por_data = {}
        for curso in cursos.values():
            dia = curso["data"]
            for id_uc, nome_uc, horas in curso["ucs"]:
                restante = horas
                while restante > 0:
                    if dia.weekday() < 5:
                        chave = dia.isoformat()
                        cor = self._cor_da_uc(id_uc)
                        self._ucs_por_data.setdefault(chave, []).append(
                            (nome_uc, curso["nome"], cor)
                        )
                        restante -= 3  # 3 horas de aula por dia, segunda a sexta.
                    dia += timedelta(days=1)

        anos = [curso["data"].year for curso in cursos.values()]
        if anos:
            ano = max(anos)
            for indice, calendario in enumerate(calendarios, start=1):
                calendario.setCurrentPage(
                    ano, self._mes_do_calendario(calendario, indice)
                )
                for data_iso in self._ucs_por_data:
                    dia_calendario = QtCore.QDate.fromString(data_iso, "yyyy-MM-dd")
                    formato = QtGui.QTextCharFormat()
                    formato.setBackground(self._ucs_por_data[data_iso][0][2])
                    formato.setToolTip(
                        "\n".join(
                            f"{nome_curso} — {nome_uc}"
                            for nome_uc, nome_curso, _ in self._ucs_por_data[data_iso]
                        )
                    )
                    calendario.setDateTextFormat(dia_calendario, formato)

    def _abrir_conexao(self):
        return conexao.conectar()

    def salvar_curso(self):
        curso = self.txt_nome_curso.text().strip()
        carga_horaria = self.txt_tempo.text().strip()
        instrutor = self.txt_instrutor.text().strip()
        quantidade_uc = self.txt_quantidade_uc.text().strip()
        inicio = self.txt_inicio.text().strip()

        if not curso or not quantidade_uc or not inicio:
            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "Preencha o nome do curso, a quantidade de UCs e a data inicial.",
            )
            return

        try:
            data_inicio = self._ler_data_inicio(inicio)
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Data inválida", str(e))
            return

        try:
            quantidade_uc_int = int(quantidade_uc)
            if quantidade_uc_int <= 0:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "A quantidade de UCs deve ser um número inteiro maior que zero.",
            )
            return

        conn = None
        cursor = None
        try:
            conn = self._abrir_conexao()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO cursos2
                    (curso, carga_horaria, instrutor, quantidade_uc, inicio)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (curso, carga_horaria, instrutor,
                 quantidade_uc_int, data_inicio.isoformat()),
            )
            conn.commit()

            QtWidgets.QMessageBox.information(
                self, "Sucesso", "Curso cadastrado com sucesso!"
            )
            self.txt_tempo.clear()
            self.txt_nome_curso.clear()
            self.txt_instrutor.clear()
            self.txt_quantidade_uc.clear()
            self.txt_inicio.clear()
            self.carregar_relatorio()

        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            QtWidgets.QMessageBox.critical(self, "Erro no banco", str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def salvar_uc(self):
        nome_curso = self.txt_curso.text().strip()
        nome_uc = self.txt_nome_uc.text().strip()
        horas = self.txt_horas_uc.text().strip()
        posicao = self.txt_posicao.text().strip()

        if not nome_curso or not nome_uc or not horas or not posicao:
            QtWidgets.QMessageBox.warning(
                self, "Atenção", "Informe o curso e preencha todos os campos da UC!"
            )
            return

        try:
            horas_int = int(horas)
            posicao_int = int(posicao)
            if horas_int <= 0 or posicao_int <= 0:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "Horas e posição devem ser números inteiros maiores que zero.",
            )
            return

        conn = None
        cursor = None
        try:
            conn = self._abrir_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_curso FROM cursos2 WHERE curso = %s ORDER BY id_curso",
                (nome_curso,),
            )
            cursos = cursor.fetchall()
            if not cursos:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Curso não encontrado",
                    "Cadastre o curso primeiro e informe o nome exatamente como foi cadastrado.",
                )
                return
            if len(cursos) > 1:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Curso duplicado",
                    "Há mais de um curso com esse nome. Diferencie os nomes antes de cadastrar a UC.",
                )
                return
            id_curso = cursos[0][0]
            cursor.execute(
                """
                INSERT INTO grade (nome_uc, horas_uc, posicao, id_curso)
                VALUES (%s, %s, %s, %s)
                """,
                (nome_uc, horas_int, posicao_int, id_curso),
            )
            conn.commit()

            QtWidgets.QMessageBox.information(
                self, "Sucesso", "UC cadastrada com sucesso!"
            )
            self.txt_horas_uc.clear()
            self.txt_posicao.clear()
            self.txt_nome_uc.clear()
            self.carregar_calendario()

        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            QtWidgets.QMessageBox.critical(self, "Erro no banco", str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def salvar_legendas(self):
        data = self._obter_data_legenda()
        campos = [
            ("INICIO_CURSO", self.txt_aula_inaugural.text().strip()),
            ("PLANEJAMENTO", self.txt_planejamento.text().strip()),
            ("RECESSO", self.txt_recesso.text().strip()),
            ("FERIADO", self.txt_feriado.text().strip()),
            ("CAPACITACAO", self.txt_capacitacao_orientador.text().strip()),
            ("REUNIAO", self.txt_reuniao.text().strip()),
            ("ESTAGIO", self.txt_estagio.text().strip()),
            ("FINAL_CURSO", self.txt_final_curso.text().strip()),
        ]
        campos = [(tipo, texto) for tipo, texto in campos if texto]

        if not campos:
            QtWidgets.QMessageBox.warning(
                self, "Atenção", "Preencha ao menos um campo antes de cadastrar."
            )
            return

        conn = None
        cursor = None
        try:
            conn = self._abrir_conexao()
            cursor = conn.cursor()
            for tipo, texto in campos:
                cursor.execute(
                    """
                    INSERT INTO eventos (titulo, descricao, data_evento, categoria)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (tipo, texto, data, tipo),
                )
            conn.commit()

            QtWidgets.QMessageBox.information(
                self, "Sucesso", "Evento(s) cadastrado(s) com sucesso!"
            )
            for nome in (
                "txt_aula_inaugural", "txt_planejamento", "txt_recesso",
                "txt_feriado", "txt_capacitacao_orientador", "txt_reuniao",
                "txt_estagio", "txt_final_curso"
            ):
                getattr(self, nome).clear()
            self.carregar_calendario()

        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            QtWidgets.QMessageBox.critical(self, "Erro no banco", str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _obter_data_legenda(self):
        # A UI atual não possui data_inicial; usa a data do calendário selecionado.
        calendarios = self.findChildren(QtWidgets.QCalendarWidget)
        if calendarios:
            return calendarios[0].selectedDate().toPyDate()
        return QtCore.QDate.currentDate().toPyDate()

    def carregar_relatorio(self):
        conn = None
        cursor = None
        try:
            conn = self._abrir_conexao()
            cursor = conn.cursor()
            filtro = self.txt_curso_2.text().strip()

            if filtro:
                cursor.execute(
                    """
                    SELECT id_curso, curso, carga_horaria, instrutor
                    FROM cursos2
                    WHERE curso LIKE %s
                    ORDER BY id_curso DESC
                    """,
                    (f"%{filtro}%",),
                )
            else:
                cursor.execute(
                    """
                    SELECT id_curso, curso, carga_horaria, instrutor
                    FROM cursos2
                    ORDER BY id_curso DESC
                    """
                )

            dados = cursor.fetchall()
            self.txt_tabela.clearContents()
            self.txt_tabela.setColumnCount(4)
            self.txt_tabela.setRowCount(len(dados))
            self.txt_tabela.setHorizontalHeaderLabels(
                ["ID", "CURSO", "CARGA HORÁRIA", "INSTRUTOR"]
            )

            for linha, row in enumerate(dados):
                for coluna, valor in enumerate(row):
                    self.txt_tabela.setItem(
                        linha, coluna,
                        QtWidgets.QTableWidgetItem("" if valor is None else str(valor)),
                    )
            self.txt_tabela.resizeColumnsToContents()

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(self, "Erro no banco", str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def carregar_calendario(self):
        conn = None
        cursor = None
        try:
            conn = self._abrir_conexao()
            cursor = conn.cursor()
            cursor.execute("SELECT data_evento, titulo, descricao FROM eventos ORDER BY data_evento")
            eventos = cursor.fetchall()

            self._eventos_por_data = {}
            for data, titulo, descricao in eventos:
                chave = data.isoformat()
                self._eventos_por_data.setdefault(chave, []).append(
                    (titulo, descricao)
                )
            self._preencher_calendario_com_ucs(cursor)

        except mysql.connector.Error as e:
            # O restante da aplicação continua utilizável se a tabela ainda não existir.
            self._eventos_por_data = {}
            self._ucs_por_data = {}
            if hasattr(self, "statusbar"):
                self.statusbar.showMessage("Banco: " + str(e), 5000)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _calendario_selecionado(self):
        sender = self.sender()
        if not sender:
            return
        data = sender.selectedDate().toPyDate().isoformat()
        partes = []
        eventos = getattr(self, "_eventos_por_data", {}).get(data, [])
        partes.extend(f"{titulo}: {descricao}" for titulo, descricao in eventos)
        ucs = getattr(self, "_ucs_por_data", {}).get(data, [])
        partes.extend(f"{nome_curso} — {nome_uc}" for nome_uc, nome_curso, _ in ucs)
        if partes:
            texto = "\n".join(partes)
            QtWidgets.QToolTip.showText(QtGui.QCursor.pos(), texto, sender)

