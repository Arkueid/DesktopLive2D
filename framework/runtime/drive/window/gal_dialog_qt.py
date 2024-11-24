from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPainter
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget


class GalDialog(QMainWindow):
    MAX_WIDTH = 400

    def __init__(self, bg_color="#000000", opacity=0.8, max_width=MAX_WIDTH, font=("Arial", 14)):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.bg_color = QColor(bg_color)
        self.opacity = opacity
        self.max_width = max_width
        self.font = QFont(font[0], font[1])
        self.dialog = None
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setFont(self.font)
        self.text_label.setStyleSheet("color: white;")
        self.text_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.text_label)
        layout.setContentsMargins(10, 10, 10, 10)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.current_text = ""
        self.text_index = 0
        self.duration = 2

    def __calculate_text_size(self, text):
        self.text_label.setText(text)
        self.text_label.adjustSize()
        width = min(self.max_width, self.text_label.width()) + 20
        height = self.text_label.height() + 20
        return width, height

    def __show(self, text, x, y, w, h, duration=2):
        self.current_text = text
        self.text_index = 0
        self.duration = duration
        width, height = self.__calculate_text_size(text)
        self.setGeometry(x + w // 2 - width // 2, y + h // 2, width, height)
        self.setWindowOpacity(self.opacity)
        self.show()
        self.__update_text()

    def __update_text(self):
        if self.text_index < len(self.current_text):
            self.text_index += 1
            text_to_display = self.current_text[:self.text_index]
            self.text_label.setText(text_to_display)
            QTimer.singleShot(50, self.__update_text)
        else:
            QTimer.singleShot(self.duration * 1000, self.__stop)

    def __stop(self):
        self.close()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.bg_color)
        painter.setOpacity(self.opacity)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def trigger_from_thread(self, text, x, y, w, h, duration=2):
        self.__show(text, x, y, w, h, duration)

    def move_from_thread(self, x, y, w, h):
        self.__doMove(x, y, w, h)

    def __doMove(self, x, y, w, h):
        self.setGeometry(x + w // 2 - self.width() // 2, y + h // 2, self.width(), self.height())
