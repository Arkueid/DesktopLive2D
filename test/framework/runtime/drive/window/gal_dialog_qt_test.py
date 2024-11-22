import sys

from PySide6.QtWidgets import QMainWindow, QApplication

from temp.gal_dialog_qt import GalDialog


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dialog = GalDialog()
        self.setWindowTitle("Main Application")
        self.setGeometry(100, 100, 800, 600)
        self.show()

        # Example trigger to show dialog
        self.show_dialog()

    def show_dialog(self):
        # You can customize the position, text, and duration
        self.dialog.trigger_from_thread("This is a test message.This is a test message.This is a test message.This is a test message.This is a test message.This is a test message.This is a test message.", 300, 300, duration=3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec())