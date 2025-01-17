import ctypes


NAME_LEN = 16


def pack_payload(cmd_class, cmd_id, payload: bytes):
    class Payload(ctypes.LittleEndianStructure):
        _pack_ = 1
        _fields_ = (
            ("header", Header),
            ("payload", ctypes.c_uint8 * len(payload))
        )

    res = Payload()
    res.header.cmd_class = cmd_class
    res.header.cmd_id = cmd_id
    res.header.payload_len = len(payload)
    for i in range(len(payload)):
        res.payload[i] = payload[i]

    return res


"""
device_type
    0: "client"
    1: "uav"
"""
class DeviceInfo(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = (
        ("type", ctypes.c_uint8),
        ("name", ctypes.c_uint8 * NAME_LEN)
    )


class Header(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = (
        ("cmd_class", ctypes.c_uint8),
        ("cmd_id", ctypes.c_uint8),
        ("payload_len", ctypes.c_uint16),
    )


class CamPos(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = (
        ("x", ctypes.c_int8),
        ("y", ctypes.c_int8)
    )


class ConnectCmdIn(ctypes.LittleEndianStructure):
    """
    is used on a client side to send a connect cmd to the server
    """
    _pack_ = 1
    _fields_ = (
        ("name", ctypes.c_uint8 * NAME_LEN),
        ("port", ctypes.c_uint16)
    )


class ConnectCmdOut(ctypes.LittleEndianStructure):
    """
    is used in a server to redirect a connect cmd from the client to the device
    """
    _pack_ = 1
    _fields_ = (
        ("ip", ctypes.c_uint32),
        ("port", ctypes.c_uint16)
    )


class ConnectVideo(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = (
        ("port", ctypes.c_uint16),
    )


def get_cameras_list(payload: bytes) -> ctypes.LittleEndianStructure:
    class CamerasList(ctypes.LittleEndianStructure):
        _pack_ = 1
        _fields_ = (
            ("count", ctypes.c_uint8),
            ("devices", DeviceInfo * payload[0])
        )
    
    return CamerasList.from_buffer_copy(payload)
