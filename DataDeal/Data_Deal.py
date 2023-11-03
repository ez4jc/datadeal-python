# Data_Deal.py
import time
import struct
import numpy as np
import open3d as o3d
import vtkmodules.all as vtk
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

def convert_to_pointcloud(R_dis, L_dis, H_dis):
    # 创建一个vtkPoints对象，用于存储点云数据
    points = vtk.vtkPoints()

    for i in range(len(R_dis)):
        # 计算 x、y 和 z 坐标
        x = R_dis[i]
        y = L_dis[i]
        z = H_dis[i]

        # 将点添加到vtkPoints对象
        points.InsertNextPoint(x, y, z)

    # 创建一个vtkPolyData对象，并将vtkPoints添加到其中
    point_cloud = vtk.vtkPolyData()
    point_cloud.SetPoints(points)

    return point_cloud


def bytesToFloat(h1,h2,h3,h4):
    ba = bytearray()
    ba.append(h1)
    ba.append(h2)
    ba.append(h3)
    ba.append(h4)
    return struct.unpack("!f",ba)[0] #把字节转换成浮点数


def Datadeal():
    start = 0
    FrameNum = 16
    TargetNum = 150
    data = np.zeros((16, 1024), dtype=np.uint8)
    data2 = np.zeros(4096, dtype=np.uint8)

    R_dis = []
    L_dis = []
    H_dis = []

    client_socket = socket_link()

    while True:
        pkt_data = receive_data(client_socket)
        packet = list(pkt_data)  # 装进packet，header数据包头部信息，pkt_data数据包数据

        # 判断前12位和数据包总长度，确保数据包接收正确
        if packet[0] == 0xFF and packet[1] == 0xFF and packet[2] == 0xFF \
                and packet[3] == 0xFF and packet[4] == 0xFF and packet[5] == 0xFF \
                and packet[6] == 0x48 and packet[7] == 0x5B and packet[8] == 0x39 \
                and packet[9] == 0xC2 and packet[10] == 0x7D and packet[11] == 0xF8 \
                and len(pkt_data) == 16640:

            # 避免错位
            if packet[14] == 0:
                for i in range(16):
                    start = 16 + i * 1040  # 计算当前数据段的起始位置
                    end = start + 1024  # 计算当前数据段的结束位置
                    tmp = packet[start:end]  # 提取当前数据段
                    data[i, 0:1024] = tmp  # 将数据段放入相应的行中

                rxFrameData = np.squeeze(data.reshape(-1, 16 * 1024))

                FrameData1 = rxFrameData[0:FrameNum * 1024:4]
                FrameData2 = rxFrameData[1:FrameNum * 1024:4]
                FrameData3 = rxFrameData[2:FrameNum * 1024:4]
                FrameData4 = rxFrameData[3:FrameNum * 1024:4]

                # 转成浮点数存到data2里
                for i in range(4096):
                    data2[i] = bytesToFloat(FrameData4[i], FrameData3[i], FrameData2[i], FrameData1[i])

                # 处理坐标
                R = np.array(data2[0:TargetNum * 5:5])
                V = np.array(data2[1:TargetNum * 5:5])
                P = np.array(data2[2:TargetNum * 5:5])
                A = np.array(data2[3:TargetNum * 5:5])
                E = np.array(data2[4:TargetNum * 5:5])
                P_cal = np.pi * P / 180.0
                E_cal = np.pi * E / 180.0
                R_cal = R * np.cos(E_cal)
                H_cal = R * np.sin(E_cal)
                R_dis = R_cal * np.cos(P_cal)
                L_dis = R_cal * np.sin(P_cal)
                H_dis = H_cal

                point_cloud = convert_to_pointcloud(R_dis, L_dis, H_dis)

                # 打印每个点云对象的坐标
                # for point in pcd.points:
                #     x, y, z = point
                #     print(f"点云对象坐标：({x}, {y}, {z})")

                points = point_cloud.GetPoints()
                num_points = points.GetNumberOfPoints()

                for i in range(num_points):
                    x, y, z = points.GetPoint(i)
                    print(f"点云对象坐标：({x}, {y}, {z})")

                #o3d.io.write_point_cloud("F:/data/test.pcd", pcd)
                writer = vtk.vtkPLYWriter()
                writer.SetFileName("F:/data/test.ply")
                writer.SetInputData(point_cloud)
                writer.SetFileTypeToASCII()
                writer.Write()

        else:
            print("等待接收数据...")


        time.sleep(1)  # 休眠1秒

"""测试调用"""
import threading
t1 = threading.Thread(target=Datadeal)
t1.start()
t1.join()