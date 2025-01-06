import socket
import threading

from ctypes import sizeof

from protocol import DeviceInfo, Header, ConnectCmdIn, pack_payload, ConnectCmdOut


is_exit = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(1)
sock.bind(("0.0.0.0", 7777))
connections = []
cameras = []


def remove_conn(sock, client_type):
    if client_type == 0:
        for i, c in enumerate(connections):
            if c["sock"] == sock:
                connections.pop(i)
    elif client_type == 1:
        for i, c in enumerate(cameras):
            if c["sock"] == sock:
                cameras.pop(i)


def handle_connection(sock: socket.socket, addr, client):
    print(f"client type {client.type} name \"{''.join([chr(c) for c in client.name])}\" addr {addr}")
    while not is_exit:
        try:
            data = sock.recv(sizeof(Header))
        except socket.timeout:
            continue

        if not data:
            break  # socket was closed
        
        header = Header.from_buffer_copy(data)
        if (header.payload_len):
            try:
                data = sock.recv(header.payload_len)
            except socket.timeout:
                continue

        # process cmd
        if client.type == 0:  # 0 is client, 1 is camera
            if header.cmd_class == 2 and header.cmd_id == 1 and header.payload_len == len(data):
                # send a connect command to the camera with the name match
                payload = ConnectCmdIn.from_buffer_copy(data)
                name = ''.join([chr(c) for c in filter(lambda c: True if 33 <= c <= 126 else False, [c for c in payload.name])]).strip()
                for cam in cameras:
                    cam_name = ''.join([chr(c) for c in filter(lambda c: True if 33 <= c <= 126 else False, [c for c in cam["client"].name])]).strip()
                    if name == cam_name:
                        data = ConnectCmdOut()
                        data.port = payload.port
                        data.ip = int.from_bytes(socket.inet_pton(socket.AF_INET, addr[0]), "little")
                        cam["sock"].sendall(pack_payload(2, 1, bytes(data)))
                        break
            elif header.cmd_class == 1 and header.cmd_id == 2 and header.payload_len == 0:
                # return a list of DeviceInfo with connected cameras
                devices_to_pack = b''.join([len(cameras).to_bytes(1, "little")] + [bytes(cam["client"]) for cam in cameras])
                data = pack_payload(1, 2, devices_to_pack)
                sock.sendall(data)
    sock.close()
    remove_conn(sock, client.type)


def listener():
    sock.listen(5)
    while not is_exit:
        try:
            client_socket, client_address = sock.accept()
        except socket.timeout:
            continue
        except Exception as e:
            print(e)
            continue

        client_socket.settimeout(1)
        try:
            client_header = Header.from_buffer_copy(client_socket.recv(sizeof(Header)))
        except Exception as e:
            print(e)
            client_socket.close()
            continue

        if client_header.cmd_class == 1 and client_header.cmd_id == 1 and client_header.payload_len == sizeof(DeviceInfo):
            try:
                client = DeviceInfo.from_buffer_copy(client_socket.recv(sizeof(DeviceInfo)))
            except Exception as e:
                print(e)
                client_socket.close()
                continue

            thread = threading.Thread(target=handle_connection, args=(client_socket, client_address, client))
            if client.type == 0:  # 0 is client, 1 is camera
                connections.append({"sock": client_socket, "addr": client_address, "client": client, "thread": thread})
            elif client.type == 1:
                cameras.append({"sock": client_socket, "addr": client_address, "client": client, "thread": thread})
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
