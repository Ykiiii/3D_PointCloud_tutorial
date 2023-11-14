# import open3d as o3d
# import numpy as np
# if __name__ =="__main__":
#     points = np.random.rand(10000, 3)
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(points)
#     o3d.visualization.draw_geometries([pcd])
# if __name__ =="__main__":
#     datadir = "J:\Document\Coding\PointCloud\cloudRgb_00000.ply"
#     pcd = o3d.io.read_point_cloud(datadir)
#     o3d.visualization.draw(pcd)

import open3d as o3d
import cv2

if __name__ =="__main__":
    datadir = "E:\\program\\GitCode\\3D_PointCloud\\PointCloud\\rectangle.ply"
    pcd = o3d.io.read_point_cloud(datadir)
    # print(pcd)
    hull, idx = pcd.compute_convex_hull()
    hull_cloud = pcd.select_by_index(idx)
    o3d.io.write_point_cloud("hull_cloud.pcd", hull_cloud)
    hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
    hull_ls.paint_uniform_color((1,0,0))
    o3d.visualization.draw_geometries([pcd,hull_ls])

