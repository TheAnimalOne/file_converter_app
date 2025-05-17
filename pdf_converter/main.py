import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QComboBox,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QFileDialog,
    QAbstractItemView,
)
from file_manager import FileManager, ConversionType

WINDOW_SIZE: tuple[int, int] = (750, 500)


class FileConverterWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.fm = FileManager()
        self.setWindowTitle("FileConverter")
        # self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])

        self.layout = QVBoxLayout()
        h_box1 = QHBoxLayout()
        self.layout.addLayout(h_box1)

        # label choose a conversion output format (0, 1)
        h_box1.addWidget(QLabel("Select Conversion Format"), alignment=Qt.AlignmentFlag.AlignCenter)
        # dropdown selection conversion options (1, 1)
        self._create_conversion_options_dropdown()
        # display for existing files (2, 1)
        self._create_file_display()
        # add new files (3, 1)
        self._add_files_button()
        h_box2 = QHBoxLayout()
        # switch file order (4, 0)
        self._switch_file_but(h_box2)
        # delete selected files (4, 1)
        self._del_file_but(h_box2)
        # clear files (4, 2)
        self._clear_files_but(h_box2)
        self.layout.addLayout(h_box2)
        # convert button (5, 1)
        # self._convert_but()
        # testing
        but = QPushButton("check selected")
        but.clicked.connect(self.test)
        self.layout.addWidget(but)

        self.setLayout(self.layout)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def test(self):
        print(self.files_list.selectedItems())

    def _create_conversion_options_dropdown(self):
        conversion_options = QComboBox()
        conversion_options.addItems(ConversionType)
        self.layout.addWidget(conversion_options)

        self.conversion_options = conversion_options

    def _add_files_button(self):
        but = QPushButton("Browse")
        but.clicked.connect(self.open_file_selector)
        self.layout.addWidget(but)
        self.add_files_button = but

    def _create_file_display(self):
        l = QListWidget()
        l.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.layout.addWidget(l)
        self.files_list = l

    def open_file_selector(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            r"C:/",
            "Images (*.png *.jpg)"
        )
        if filenames:
            self.fm.add_file_path(filenames)
            self.files_list.addItems(self.fm.display_files())

    def _switch_file_but(self, but_layout):
        but = QPushButton("Swap Files")
        but.clicked.connect(self.switch_file_order)
        but_layout.addWidget(but)

    def switch_file_order(self):
        if len(self.files_list.selectedItems()) == 2:
            i, j = self.files_list.selectedIndexes()
            self.fm.switch_order(i.row(), j.row())
            self.files_list.clear()
            self.files_list.addItems(self.fm.display_files())
        else:
            return None

    def _del_file_but(self, but_layout):
        but = QPushButton("Delete Files")
        but.clicked.connect(self.delete_files)
        but_layout.addWidget(but)

    def delete_files(self):
        self.fm.delete_file_path([i.row() for i in self.files_list.selectedIndexes()])
        self.files_list.clear()
        self.files_list.addItems(self.fm.display_files())

    def _clear_files_but(self, but_layout):
        but = QPushButton("Clear All")
        but.clicked.connect(self.clear_all_files)
        but_layout.addWidget(but)

    def clear_all_files(self):
        self.fm.clear_file_paths()
        self.files_list.clear()

def main():
    file_converter_app = QApplication([])
    file_converter_window = FileConverterWindow()
    file_converter_window.show()
    sys.exit(file_converter_app.exec())

if __name__ == "__main__":
    main()