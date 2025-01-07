import socket

from ..designs.main_window_widget import Ui_MainWindow
from protocol import pack_payload, DeviceInfo, Header, get_cameras_list, ConnectCmdIn, CamPos
from ctypes import sizeof

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QThread, pyqtSignal


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cam_conn_state = False
        self.cam_conn_tcp = None
        self.client_socket = None
        self.client_address = None
        self.cam_conn_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_conn_state = False
        self.server_conn_tcp = None

    def connect_camera(self):
        if not self.cam_conn_state:
            # open sockets
            self.cam_conn_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cam_conn_tcp.settimeout(5)
            self.cam_conn_tcp.bind(("0.0.0.0", 7778))
            self.cam_conn_tcp.listen(1)

            # send connection command over the server for reverse connection from the camera to this program
            data = ConnectCmdIn()
            for i, c in enumerate(self.camera_name.currentText().encode()):
                data.name[i] = c
            data.port = 7778
            data = pack_payload(2, 1, bytes(data))
            self.server_conn_tcp.sendall(data)

            try:
                # wait for the connection
                self.client_socket, self.client_address = self.cam_conn_tcp.accept()
            except socket.timeout:
                self.statusBar().showMessage("Час очікування підключення вичерпано. Немає підключень.")
                self.cam_conn_tcp.close()
                self.cam_conn_tcp = None
            except Exception as e:
                self.statusBar().showMessage(f"Невідома помилка: {e}")
            else:
                self.camera_name.setEnabled(False)
                self.camera_password.setEnabled(False)
                self.server_connect_btn.setEnabled(False)
                self.camera_connect_btn.setText("Disconnect")
                self.cam_conn_state = True
                self.statusBar().showMessage(f"Камера {self.camera_name.currentText()} підключена")

                # start connection handler
                pass
        else:
            if self.cam_conn_tcp:
                self.cam_conn_tcp.close()  # close connection
                self.client_socket.close()
            self.camera_name.setEnabled(True)
            self.camera_password.setEnabled(True)
            self.server_connect_btn.setEnabled(True)
            self.camera_connect_btn.setText("Connect")

            self.cam_conn_state = False

    def connect_server(self):
        if not self.server_conn_state:
            ip, port = self.server_ip.text().strip().split(':')
            self.server_conn_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_conn_tcp.settimeout(3)
            try:
                self.server_conn_tcp.connect((ip, int(port)))
            except socket.timeout:
                self.statusBar().showMessage(f"Помилка: час підключення до {ip}:{port} вичерпано (timeout).")
            except socket.gaierror:
                self.statusBar().showMessage(f"Помилка: не вдалося знайти адресу {ip}. Перевірте правильність імені хоста.")
            except ConnectionRefusedError:
                self.statusBar().showMessage(f"Помилка: сервер {ip}:{port} відмовився від з'єднання.")
            except Exception as e:
                self.statusBar().showMessage(f"Невідома помилка: {e}")
            else:
                self.camera_connect_btn.setEnabled(True)
                self.server_ip.setEnabled(False)
                self.server_password.setEnabled(False)
                self.server_connect_btn.setText("Disconnect")

                # auth
                self.server_conn_state = True
                data = DeviceInfo()
                data.type = 0
                for i, c in enumerate("client name".encode()):
                    data.name[i] = c
                data = pack_payload(1, 1, bytes(data))
                self.server_conn_tcp.sendall(data)

                # fetch cameras list
                self.refresh_cam_list()

        else:
            if self.server_conn_tcp:
                self.server_conn_tcp.close()
            self.server_ip.setEnabled(True)
            self.server_password.setEnabled(True)
            self.server_connect_btn.setText("Connect")
            self.camera_connect_btn.setEnabled(False)

            self.server_conn_state = False

    def ctrl_val_update(self):
        if self.cam_conn_tcp and self.cam_conn_state:
            data = CamPos()
            data.x = self.x_slider.value()
            data.y = self.y_slider.value()
            data = pack_payload(3, 1, bytes(data))
            self.client_socket.sendall(data)

    def connection_handler(self):
        pass

    def refresh_cam_list(self):
        data = Header()
        data.cmd_class = 1
        data.cmd_id = 2
        data.payload_len = 0
        self.server_conn_tcp.sendall(data)

        try:  # get header
            data = self.server_conn_tcp.recv(sizeof(Header))
            header = Header.from_buffer_copy(data)
        except socket.timeout:
            self.statusBar().showMessage("Помилка: таймаут отримання заголовку списку камер")
            return
        except Exception as e:
            self.statusBar().showMessage(f"Невідома помилка: {e}")
            return

        if header.cmd_class == 1 and header.cmd_id == 2:
            try:  # get payload
                data = self.server_conn_tcp.recv(header.payload_len)
                payload = get_cameras_list(data)
            except socket.timeout:
                self.statusBar().showMessage("Помилка: таймаут отримання списку камер")
                return
            except Exception as e:
                self.statusBar().showMessage(f"Невідома помилка: {e}")
                return

            self.camera_name.clear()
            for cam in payload.devices:
                name = ''.join([chr(c) for c in filter(lambda c: True if 33 <= c <= 126 else False, [c for c in cam.name])]).strip()
                self.camera_name.addItem(name)
            self.statusBar().showMessage(f"Отримано {payload.count} камер")


class UdpListenerThread(QThread):
    message_received = pyqtSignal(bytes)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind("0.0.0.0", self.port)
        sock.settimeout(1)
        while self.running:
            try:
                data = sock.recv(1024)
            except socket.timeout:
                continue

            self.message_received.emit(data)

            if not data:
                self.stop()  # socket was closed
        sock.close()

    def stop(self):
        self.running = False
        self.wait()
