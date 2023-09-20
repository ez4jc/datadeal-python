# main.py
from DataDeal.data_receiver import receive_data
from DataDeal.data_processor import convert_to_pointcloud
import time


def main():
    while True:
        # 接收数据，此处假设接收到的数据是一个包含[距离, 水平角度, 垂直角度]的列表
        received_data = receive_data()

        if received_data is not None:
            distance, horizontal_angle, vertical_angle = received_data
            point_cloud = convert_to_pointcloud(distance, horizontal_angle, vertical_angle)
            print(f"第一个点的坐标：{point_cloud[0]}")  # 打印第一个点的坐标
        else:
            print("等待接收数据...")

        time.sleep(1)  # 休眠1秒


if __name__ == "__main__":
    main()
