import pcl
import numpy as np
import math

def convert_to_pointcloud(distance, horizontal_angle, vertical_angle):
    # 计算 x、y 和 z 坐标
    horizontal_angle_rad = math.radians(horizontal_angle)
    vertical_angle_rad = math.radians(vertical_angle)
    x = distance * math.sin(vertical_angle_rad) * math.cos(horizontal_angle_rad)
    y = distance * math.sin(vertical_angle_rad) * math.sin(horizontal_angle_rad)
    z = distance * math.cos(vertical_angle_rad)

    # 创建一个包含一个点的2D numpy 数组
    point = np.array([[x, y, z]], dtype=np.float32)

    # 创建一个 pcl 点云对象
    cloud = pcl.PointCloud()
    cloud.from_array(point)

    # 返回点云对象
    return cloud
