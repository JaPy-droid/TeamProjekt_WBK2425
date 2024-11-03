import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d

bunny = o3d.data.BunnyMesh()
mesh = o3d.io.read_triangle_mesh(bunny.path)
mesh.compute_vertex_normals()

pcd = mesh.sample_points_poisson_disk(750)
o3d.visualization.draw_geometries([pcd])

pcd.normals = o3d.utility.Vector3dVector(np.zeros(
    (1, 3)))  # invalidate existing normals
pcd.estimate_normals()
o3d.visualization.draw_geometries([pcd], point_show_normal=True)

print("test")