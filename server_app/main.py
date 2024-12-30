import socket
import threading
import ctypes


is_exit = False


class DeviceInfo(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = (
        ("type", ctypes.c_uint8),
        ("name", ctypes.c_uint8 * 23)
    )


def handle_connection(sock: socket.socket, addr, client):
    print(f"client type {client.type} name {client.name} addr {addr}")
    while not is_exit:
        data = sock.recv(20)
        if not data:
            break  # socket was closed
        print(data)
    sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(1)
sock.bind(("0.0.0.0", 7777))
connections = []


def listener():
    sock.listen(1)
    while not is_exit:
        try:
            client_socket, client_address = sock.accept()
        except socket.timeout:
            continue
        except Exception as e:
            print(e)
            continue
        client = DeviceInfo.from_buffer_copy(client_socket.recv(ctypes.sizeof(DeviceInfo)))
        thread = threading.Thread(target=handle_connection, args=(client_socket, client_address, client))
        connections.append({"sock": client_socket, "addr": client_address, "client": client, "thread": thread})
        thread.start()


listener_th = threading.Thread(target=listener)
listener_th.start()

while not is_exit:
    cmd = input(">>> ")
    if cmd == "exit":
        is_exit = True
        listener_th.join()
        for con in connections:
            con["thread"].join()
