import open3d as o3d

def convert_to_pointcloud(R_dis, L_dis, H_dis):
    pcd = o3d.geometry.PointCloud()
    points = []
    for i in range(len(R_dis)):
        # 计算 x、y 和 z 坐标
        x = R_dis[i]
        y = L_dis[i]
        z = H_dis[i]
        points.append([x, y, z])

    pcd.points = o3d.utility.Vector3dVector(points)

    # 返回点云对象的列表
    return pcd


