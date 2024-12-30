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
        ("x", ctypes.c_uint8),
        ("y", ctypes.c_uint8)
    )


class ConnectCmd(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = (
        ("name", ctypes.c_uint8 * NAME_LEN)
    )
