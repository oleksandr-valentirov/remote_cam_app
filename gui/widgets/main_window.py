from ..designs.main_window_widget import Ui_MainWindow

from PyQt6.QtWidgets import QMainWindow


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.conn_state = False
        self.conn = None

    def connect(self):
        if not self.conn_state:
            self.ip_addr.setEnabled(False)
            self.password.setEnabled(False)
            self.connect_btn.setText("Disconnect")

            self.conn_state = True
        else:
            if self.conn:
                pass  # close connection
            self.ip_addr.setEnabled(True)
            self.password.setEnabled(True)
            self.connect_btn.setText("Connect")

            self.conn_state = False

    def connection_handler(self):
        pass
