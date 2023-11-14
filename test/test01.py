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

# import open3d as o3d
# import cv2

# if __name__ =="__main__":
#     datadir = "PointCloudData\\yk_examples\\rectangle.ply"
#     pcd = o3d.io.read_point_cloud(datadir)
#     # print(pcd)
#     hull, idx = pcd.compute_convex_hull()
#     hull_cloud = pcd.select_by_index(idx)
#     o3d.io.write_point_cloud("hull_cloud.pcd", hull_cloud)

#     hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
#     hull_ls.paint_uniform_color((1,0,0))
#     o3d.visualization.draw_geometries([pcd,hull_ls])


import open3d as o3d
import numpy as np

def edges_to_lineset(mesh, edges, color):
    """将边缘转为线集"""
    ls = o3d.geometry.LineSet()
    ls.points = mesh.vertices
    ls.lines = edges
    colors = np.empty((np.asarray(edges).shape[0], 3))
    colors[:] = color
    ls.colors = o3d.utility.Vector3dVector(colors)
    return ls
 
 
def check_properties(name, mesh):
    # 计算顶点法线
    mesh.compute_vertex_normals()
    # 是否为边缘流形（考虑边界）
    edge_manifold = mesh.is_edge_manifold(allow_boundary_edges=True)
    # 是否为边缘流形（不考虑边界）
    edge_manifold_boundary = mesh.is_edge_manifold(allow_boundary_edges=False)
    # 是否为所有顶点是否为流形
    vertex_manifold = mesh.is_vertex_manifold()
    # 是否为自相交网格
    self_intersecting = mesh.is_self_intersecting()
    # 是否为水密网格
    watertight = mesh.is_watertight()
    # 是否为可定向的网格
    orientable = mesh.is_orientable()
 
    print(name)
    print(f"  edge_manifold:          {edge_manifold}")
    print(f"  edge_manifold_boundary: {edge_manifold_boundary}")
    print(f"  vertex_manifold:        {vertex_manifold}")
    print(f"  self_intersecting:      {self_intersecting}")
    print(f"  watertight:             {watertight}")
    print(f"  orientable:             {orientable}")
 
    geoms = [mesh]
    # 获取非边缘流形几何（考虑边界）
    if not edge_manifold:
        edges = mesh.get_non_manifold_edges(allow_boundary_edges=True)
        geoms.append(edges_to_lineset(mesh, edges, (1, 0, 0)))
    # 获取非边缘流形几何（不考虑边界）
    if not edge_manifold_boundary:
        edges = mesh.get_non_manifold_edges(allow_boundary_edges=False)
        geoms.append(edges_to_lineset(mesh, edges, (0, 1, 0)))
    # 获取非顶点流形
    if not vertex_manifold:
        verts = np.asarray(mesh.get_non_manifold_vertices())
        pcl = o3d.geometry.PointCloud(
            points=o3d.utility.Vector3dVector(np.asarray(mesh.vertices)[verts]))
        pcl.paint_uniform_color((0, 0, 1))
        geoms.append(pcl)
    # 自相交网格
    if self_intersecting:
        intersecting_triangles = np.asarray(
            mesh.get_self_intersecting_triangles())
        intersecting_triangles = intersecting_triangles[0:1]
        intersecting_triangles = np.unique(intersecting_triangles)
        print("  # visualize self-intersecting triangles")
        triangles = np.asarray(mesh.triangles)[intersecting_triangles]
        edges = [
            np.vstack((triangles[:, i], triangles[:, j]))
            for i, j in [(0, 1), (1, 2), (2, 0)]
        ]
        edges = np.hstack(edges).T
        edges = o3d.utility.Vector2iVector(edges)
        geoms.append(edges_to_lineset(mesh, edges, (1, 0, 1)))
    o3d.visualization.draw_geometries(geoms, mesh_show_back_face=True)
 
 
def get_non_manifold_edge_mesh():
    verts = np.array(
        [[-1, 0, 0], [0, 1, 0], [1, 0, 0], [0, -1, 0], [0, 0, 1]],
        dtype=np.float64,
    )
    triangles = np.array([[0, 1, 3], [1, 2, 3], [1, 3, 4]])
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(verts)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    mesh.compute_vertex_normals()
    mesh.rotate(
        mesh.get_rotation_matrix_from_xyz((np.pi / 4, 0, np.pi / 4)),
        center=mesh.get_center(),
    )
    return mesh
 
 
def get_non_manifold_vertex_mesh():
    verts = np.array(
        [
            [-1, 0, -1],
            [1, 0, -1],
            [0, 1, -1],
            [0, 0, 0],
            [-1, 0, 1],
            [1, 0, 1],
            [0, 1, 1],
        ],
        dtype=np.float64,
    )
    triangles = np.array([
        [0, 1, 2],
        [0, 1, 3],
        [1, 2, 3],
        [2, 0, 3],
        [4, 5, 6],
        [4, 5, 3],
        [5, 6, 3],
        [4, 6, 3],
    ])
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(verts)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    mesh.compute_vertex_normals()
    mesh.rotate(
        mesh.get_rotation_matrix_from_xyz((np.pi / 4, 0, np.pi / 4)),
        center=mesh.get_center(),
    )
    return mesh
 
 
def get_open_box_mesh():
    mesh = o3d.geometry.TriangleMesh.create_box()
    mesh.triangles = o3d.utility.Vector3iVector(np.asarray(mesh.triangles)[:-2])
    mesh.compute_vertex_normals()
    mesh.rotate(
        mesh.get_rotation_matrix_from_xyz((0.8 * np.pi, 0, 0.66 * np.pi)),
        center=mesh.get_center(),
    )
    return mesh
 
 
def get_intersecting_boxes_mesh():
    mesh0 = o3d.geometry.TriangleMesh.create_box()
    T = np.eye(4)
    T[:, 3] += (0.5, 0.5, 0.5, 0)
    mesh1 = o3d.geometry.TriangleMesh.create_box()
    mesh1.transform(T)
    mesh = mesh0 + mesh1
    mesh.compute_vertex_normals()
    mesh.rotate(
        mesh.get_rotation_matrix_from_xyz((0.7 * np.pi, 0, 0.6 * np.pi)),
        center=mesh.get_center(),
    )
    return mesh
 
if __name__ =="__main__":
    mesh = o3d.io.read_triangle_mesh("PointCloudData/yk_examples/t_pipe.ply")
    check_properties('Knot', mesh)
    # check_properties('Moebius', o3d.geometry.TriangleMesh.create_moebius(twists=1))
    check_properties("non-manifold edge", get_non_manifold_edge_mesh())
    check_properties("non-manifold vertex", get_non_manifold_vertex_mesh())
    check_properties("open box", get_open_box_mesh())
    check_properties("intersecting_boxes", get_intersecting_boxes_mesh())