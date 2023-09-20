import socket

def receive_data():
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

    def parse_double_data(data_str):
        try:
            # 分割字符串并将其转换为 double 数值
            parts = data_str.split()
            if len(parts) == 3:
                double_array = [float(parts[0]), float(parts[1]), float(parts[2])]
                return double_array
            else:
                return None
        except ValueError:
            return None

    # 等待客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # 接收字符串数据
    data = client_socket.recv(1024).decode("utf-8")  # 接收数据并解码

    # 解析字符串数据为 double 数组
    double_data = parse_double_data(data)

    # 关闭客户端连接
    client_socket.close()

    # 关闭服务器套接字
    server_socket.close()

    return double_data