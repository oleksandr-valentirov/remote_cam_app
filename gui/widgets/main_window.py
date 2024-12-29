from ..designs.main_window_widget import Ui_MainWindow

from PyQt6.QtWidgets import QMainWindow


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
