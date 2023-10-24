import socket

def socket_link():
    # 服务器的IP地址和端口（与发送端程序中的设置匹配）

    #server_ip = "192.168.31.79"  # 两台电脑测试用
    server_ip = "127.0.0.1"  # IP地址
    server_port = 8080      # 端口号

    # 创建套接字并绑定到指定的IP地址和端口
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))

    # 监听连接
    server_socket.listen(1)
    print(f"Listening on {server_ip}:{server_port}...")

    # 等待客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    return client_socket

def receive_data(client_socket):

    # 接收字符串数据
    data = client_socket.recv(16640)  # 接收数据

    return data