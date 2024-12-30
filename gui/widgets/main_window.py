import socket

from ..designs.main_window_widget import Ui_MainWindow

from PyQt6.QtWidgets import QMainWindow


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cam_conn_state = False
        self.cam_conn_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cam_conn_tcp.settimeout(5)
        self.cam_conn_tcp.bind(("0.0.0.0", 7778))
        self.client_socket = None
        self.client_address = None
        self.cam_conn_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_conn_state = False
        self.server_conn_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_camera(self):
        if not self.cam_conn_state:
            # open sockets
            self.cam_conn_tcp.listen(1)

            # send connection command over the server for reverse connection from the camera to this program
            pass

            try:
                # wait for the connection
                self.client_socket, self.client_address = self.cam_conn_tcp.accept()
            except socket.timeout:
                self.statusBar().showMessage("Час очікування підключення вичерпано. Немає підключень.")
            except Exception as e:
                self.statusBar().showMessage(f"Невідома помилка: {e}")
            else:
                self.camera_name.setEnabled(False)
                self.camera_password.setEnabled(False)
                self.server_connect_btn.setEnabled(False)
                self.camera_connect_btn.setText("Disconnect")
                self.cam_conn_state = True

                # start connection handler
                pass
        else:
            if self.cam_conn_tcp:
                self.cam_conn_tcp.close()  # close connection
            self.camera_name.setEnabled(True)
            self.camera_password.setEnabled(True)
            self.server_connect_btn.setEnabled(True)
            self.camera_connect_btn.setText("Connect")

            self.cam_conn_state = False

    def connect_server(self):
        if not self.server_conn_state:
            ip, port = self.server_ip.text().strip().split(':')
            try:
                self.server_conn_tcp.connect((ip, port))
                self.server_ip.setEnabled(False)
                self.server_password.setEnabled(False)
                self.server_connect_btn.setText("Disconnect")
                self.server_conn_state = True
            except socket.timeout:
                self.statusBar().showMessage(f"Помилка: час підключення до {ip}:{port} вичерпано (timeout).")
            except socket.gaierror:
                self.statusBar().showMessage(f"Помилка: не вдалося знайти адресу {ip}. Перевірте правильність імені хоста.")
            except ConnectionRefusedError:
                self.statusBar().showMessage(f"Помилка: сервер {ip}:{port} відмовився від з'єднання.")
            except Exception as e:
                self.statusBar().showMessage(f"Невідома помилка: {e}")
        else:
            if self.server_conn_tcp:
                self.server_conn_tcp.close()
            self.server_ip.setEnabled(True)
            self.server_password.setEnabled(True)
            self.server_connect_btn.setText("Connect")

            self.server_conn_state = False

    def connection_handler(self):
        pass
