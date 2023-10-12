import pcl
import numpy as np
import math

def convert_to_pointcloud(R_dis, L_dis, H_dis):
    point_clouds = []  # 存储点云对象的列表

    for i in range(len(R_dis)):
        # 计算 x、y 和 z 坐标
        x = R_dis[i]
        y = L_dis[i]
        z = H_dis[i]

        # 创建一个包含一个点的2D numpy 数组
        point = np.array([[x, y, z]], dtype=np.float32)

        # 创建一个 pcl 点云对象
        cloud = pcl.PointCloud()
        cloud.from_array(point)

        # 将点云对象添加到列表中
        point_clouds.append(cloud)

    # 返回点云对象的列表
    return point_clouds
