import sys

from PyQt6.QtWidgets import QApplication
from file_converter_window import FileConverterWindow


def main():
    file_converter_app = QApplication([])
    file_converter_window = FileConverterWindow()
    file_converter_window.show()
    sys.exit(file_converter_app.exec())

if __name__ == "__main__":
    main()