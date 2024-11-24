from PySide6.QtWidgets import QWidget, QVBoxLayout

from qfluentwidgets import SingleDirectionScrollArea


class ScrollDesign(QWidget):

    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        scroll_area = SingleDirectionScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea{background: transparent; border: none}")

        view = QWidget()
        view.setStyleSheet("QWidget{background: transparent}")

        self.vBoxLayout = QVBoxLayout(view)

        scroll_area.setWidget(view)
        vbox.addWidget(scroll_area)
        self.setLayout(vbox)

        self.vBoxLayout.setContentsMargins(10, 10, 20, 10)


