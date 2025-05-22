import sys
import ctypes

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from classes.file_converter_window import FileConverterWindow

APP_ID = u'file_converter_app.v1.0.0'


def main():
    print("Starting App!")
    # add logo to bar
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
    file_converter_app = QApplication([])
    # add logo
    file_converter_app.setWindowIcon(QIcon("classes/convertible.png"))
    # set dark mode
    file_converter_app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    file_converter_window = FileConverterWindow()
    file_converter_window.show()
    sys.exit(file_converter_app.exec())

if __name__ == "__main__":
    main()
