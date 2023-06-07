import socket


def get_internal_ip():
    """
    获取IP地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_free_port():
    """
    获取空闲Port
    :return:
    """
    try:
        s = socket.socket()
        s.bind(('', 0))
        ip, port = s.getsockname()
    finally:
        s.close()

    return port