import vtkmodules.all as vtk

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


