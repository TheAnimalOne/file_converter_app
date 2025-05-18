from enum import StrEnum
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QLayout,
    QComboBox,
    QMainWindow,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QAbstractItemView,
)
from file_converter import (
    FileConverter,
    ConversionType,
    ConversionOutcome,
)


class ButtonName(StrEnum):
    ADD_FILES = "Browse"
    SWITCH = "Swap Files"
    DELETE = "Delete Files"
    CLEAR = "Clear All"
    CONVERT = "Convert"


APP_NAME = "FileConverter"


class FileConverterWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.fc = FileConverter()
        self.setWindowTitle(APP_NAME)

        self.layout = QVBoxLayout()

        # label choose a conversion output format (0, 1)
        self.layout.addWidget(QLabel("Select Conversion Format"), alignment=Qt.AlignmentFlag.AlignCenter)
        # dropdown selection conversion options (1, 1)
        self._create_conversion_options_dropdown()
        # display for existing files (2, 1)
        self._create_file_display()
        # add new files (3, 1)
        self._create_button(ButtonName.ADD_FILES, self.open_file_selector, self.layout)
        h_box = QHBoxLayout()
        # switch file order (4, 0)
        self._create_button(ButtonName.SWITCH, self.switch_file_order, h_box)
        # delete selected files (4, 1)
        self._create_button(ButtonName.DELETE, self.delete_files, h_box)
        # clear files (4, 2)
        self._create_button(ButtonName.CLEAR, self.clear_all_files, h_box)
        self.layout.addLayout(h_box)
        # convert button (5, 1)
        self._create_button(ButtonName.CONVERT, self.open_dir_selector, self.layout)
        self.setLayout(self.layout)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def _create_button(self, name: str, connected_func: Callable, layout: QLayout) -> None:
        but = QPushButton(name)
        but.clicked.connect(connected_func)
        layout.addWidget(but)

    def _refresh_display(self) -> None:
        # "refresh" the display by clearing the QListWidget and reassigning it the file converter's display list
        self.files_list.clear()
        self.files_list.addItems(self.fc.display_files())

    def _create_conversion_options_dropdown(self) -> None:
        conversion_options = QComboBox()
        conversion_options.addItems(ConversionType)
        self.layout.addWidget(conversion_options)

        self.conversion_options = conversion_options

    def _create_file_display(self) -> None:
        l = QListWidget()
        l.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.layout.addWidget(l)
        self.files_list = l

    def open_file_selector(self) -> None:
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            r"C:/",
            "Images (*.png *.jpg)"
        )
        if filenames:
            # add new paths to the file converter class and refresh the display list
            self.fc.add_file_path(filenames)
            self._refresh_display()

    def open_dir_selector(self) -> None:
        dir_sel = QFileDialog()
        dir_sel.setFileMode(QFileDialog.FileMode.Directory)
        dir_name = dir_sel.getExistingDirectory(
            self,
            "Select Directory",
            r"C:/",
        )
        if dir_name:
            # create pop up box to notify conversion status
            msg_type, msg_content = self.fc.convert_files(self.conversion_options.currentText(), dir_name)
            # bring up msg in box
            pop_up = QMessageBox()
            pop_up.setWindowTitle(msg_type)
            pop_up.setText(msg_content)
            pop_up.exec()
            # clear files if successfully converted files
            if msg_type == ConversionOutcome.SUCCESS:
                self.clear_all_files()

    def switch_file_order(self) -> None:
        # only switch files if there are exactly 2 items selected in list
        if len(self.files_list.selectedItems()) == 2:
            i, j = self.files_list.selectedIndexes()
            self.fc.switch_order(i.row(), j.row())
            # refresh display list after switching
            self._refresh_display()
        else:
            return None

    def delete_files(self) -> None:
        self.fc.delete_file_path([i.row() for i in self.files_list.selectedIndexes()])
        self._refresh_display()

    def clear_all_files(self) -> None:
        self.fc.clear_file_paths()
        self.files_list.clear()
