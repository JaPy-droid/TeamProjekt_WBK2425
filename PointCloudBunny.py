import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d

bunny = o3d.data.BunnyMesh()
mesh = o3d.io.read_triangle_mesh(bunny.path)
mesh.compute_vertex_normals()

pcd = mesh.sample_points_poisson_disk(750)
o3d.visualization.draw_geometries([pcd])

