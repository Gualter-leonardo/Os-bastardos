from PyQt5 import QtCore, QtWidgets


class AjusteTelaPrincipal(QtCore.QObject):
    """Adapta as geometrias fixas do Designer ao tamanho atual da janela."""

    def __init__(self, janela):
        super().__init__(janela)
        self.janela = janela
        self.central = janela.centralWidget()
        self.abas = janela.findChild(QtWidgets.QTabWidget, "TAB3")
        self.largura_base = max(1, self.abas.geometry().width()) if self.abas else 1
        self.altura_base = max(1, self.abas.geometry().height()) if self.abas else 1
        self._aplicando = False
        self._conteudo = self._capturar_conteudo(self.abas) if self.abas else []
        self._definir_tamanho_minimo()
        janela.installEventFilter(self)
        QtCore.QTimer.singleShot(0, self.aplicar)

    def _definir_tamanho_minimo(self):
        if self.abas is None:
            return
        tela = QtWidgets.QApplication.primaryScreen()
        if tela is None:
            return
        disponivel = tela.availableGeometry()
        largura_base = max(1, self.abas.geometry().width())
        altura_base = max(1, self.abas.geometry().height())
        # Evita reduzir os formulários a ponto de os rótulos ficarem ilegíveis.
        # Em monitores menores, o limite acompanha a área disponível.
        largura_minima = min(
            round(largura_base * 0.65), round(disponivel.width() * 0.95)
        )
        altura_minima = min(
            round(altura_base * 0.65), round(disponivel.height() * 0.90)
        )
        self.janela.setMinimumSize(
            max(320, largura_minima), max(360, altura_minima)
        )

    def _capturar_conteudo(
        self, pai, dimensoes_base=None, preencher_raizes=False
    ):
        if pai is None:
            return []
        itens = []
        largura_base, altura_base = dimensoes_base or (
            max(1, pai.width()), max(1, pai.height())
        )
        for filho in pai.findChildren(
            QtWidgets.QWidget, options=QtCore.Qt.FindDirectChildrenOnly
        ):
            nome = filho.objectName()
            if not nome or nome.startswith("qt_"):
                continue
            fonte = filho.font()
            itens.append({
                "widget": filho,
                "geometria": filho.geometry(),
                "largura_pai": largura_base,
                "altura_pai": altura_base,
                "fonte": fonte,
                "pontos": fonte.pointSizeF(),
                "preencher_pagina": preencher_raizes,
                "raiz_pagina": preencher_raizes,
                "pixmap": (
                    filho.pixmap().copy()
                    if isinstance(filho, QtWidgets.QLabel)
                    and filho.pixmap() is not None
                    else None
                ),
                "filhos": self._capturar_conteudo(filho),
            })
        if isinstance(pai, QtWidgets.QTabWidget):
            for indice in range(pai.count()):
                pagina = pai.widget(indice)
                itens.append({
                    "widget": pagina,
                    "pagina_aba": True,
                    "aba_principal": pai is self.abas,
                    "filhos": self._capturar_conteudo(
                        pagina,
                        (max(1, pai.width()), max(1, pai.height())),
                        preencher_raizes=True,
                    ),
                })
        return itens

    def eventFilter(self, objeto, evento):
        if objeto is self.janela and evento.type() == QtCore.QEvent.Resize:
            if not self._aplicando:
                QtCore.QTimer.singleShot(0, self.aplicar)
        return False

    def aplicar(self):
        if self._aplicando or self.central is None or self.abas is None:
            return
        self._aplicando = True
        try:
            self.abas.setGeometry(self.central.rect())
            QtWidgets.QApplication.processEvents()
            self._ajustar_itens(self._conteudo)
        finally:
            self._aplicando = False

    def _ajustar_itens(
        self, itens, escala=1.0, deslocamento=(0, 0), raizes_pagina=False
    ):
        for item in itens:
            widget = item["widget"]
            if widget is None:
                continue
            if item.get("pagina_aba"):
                # O próprio QTabWidget posiciona as páginas; só ajustamos
                # os controles que estão dentro delas.
                if item.get("aba_principal"):
                    largura_pagina = max(1, widget.width())
                    altura_pagina = max(1, widget.height())
                    escala_pagina = min(
                        largura_pagina / self.largura_base,
                        altura_pagina / self.altura_base,
                    )
                    deslocamento_pagina = (
                        round((largura_pagina - self.largura_base * escala_pagina) / 2),
                        round((altura_pagina - self.altura_base * escala_pagina) / 2),
                    )
                    self._ajustar_itens(
                        item["filhos"], escala_pagina, deslocamento_pagina, True
                    )
                else:
                    self._ajustar_itens(item["filhos"], escala, (0, 0), True)
                continue
            pai = widget.parentWidget()
            if pai is None:
                continue
            g = item["geometria"]
            if item.get("preencher_pagina"):
                widget.setGeometry(pai.rect())
            else:
                dx, dy = deslocamento if raizes_pagina else (0, 0)
                widget.setGeometry(
                    round(g.x() * escala + dx),
                    round(g.y() * escala + dy),
                    max(1, round(g.width() * escala)),
                    max(1, round(g.height() * escala)),
                )
            pixmap = item.get("pixmap")
            if pixmap is not None and isinstance(widget, QtWidgets.QLabel):
                widget.setPixmap(pixmap.scaled(
                    widget.size(), QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation,
                ))
            pontos = item["pontos"]
            if pontos > 0:
                fonte = item["fonte"]
                fonte.setPointSizeF(max(6, min(18, pontos * escala)))
                widget.setFont(fonte)
            if item.get("preencher_pagina"):
                self._ajustar_itens(
                    item["filhos"], escala, deslocamento, True
                )
            else:
                self._ajustar_itens(item["filhos"], escala)


def adaptar_tela_principal(janela):
    ajuste = AjusteTelaPrincipal(janela)
    janela._ajuste_tela_principal = ajuste
    return ajuste
