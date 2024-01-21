import open3d as o3d
import numpy as np
from pathlib import Path
from .utils.load_pcd import get_points_from_pcd_file
from .utils.o3d_visualize_utils import draw_scenes as open3d_draw_scenes


class PointCloudProcess:

    @staticmethod
    def cut_pcd(points, pcd_range):
        x_range = [pcd_range[0], pcd_range[3]]
        y_range = [pcd_range[1], pcd_range[4]]
        z_range = [pcd_range[2], pcd_range[5]]
        mask = (x_range[0] <= points[:, 0]) & (points[:, 0] <= x_range[1]) & (y_range[0] < points[:, 1]) & (
                points[:, 1] <= y_range[1]) & (z_range[0] < points[:, 2]) & (points[:, 2] <= z_range[1])
        points = points[mask]
        return points

    @staticmethod
    def show_pcd(path, point_size=1, background_color=[0, 0, 0], size=(1500, 800), pcd_range=None):
        points = PointCloudProcess.get_points(path)[:, 0:3]
        if pcd_range:
            points = PointCloudProcess.cut_pcd(points, pcd_range)
        # open3d
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name='show_pcd', width=size[0], height=size[1])
        pcd = o3d.open3d.geometry.PointCloud()
        pcd.points = o3d.open3d.utility.Vector3dVector(points)
        opt = vis.get_render_option()
        opt.point_size = point_size
        opt.background_color = np.asarray(background_color)
        vis.add_geometry(pcd)
        vis.run()
        vis.clear_geometries()
        vis.destroy_window()

    @staticmethod
    def get_points(path, num_features=3):
        pcd_ext = Path(path).suffix
        if pcd_ext == '.bin':
            points = np.fromfile(path, dtype=np.float32).reshape(-1, 4)
        elif pcd_ext == ".npy":
            points = np.load(path)
        elif pcd_ext == ".pcd":
            points = get_points_from_pcd_file(path, num_features=num_features)
        else:
            raise NameError("Unable to handle {} formatted files".format(pcd_ext))
        return points[:, 0:num_features]

    @staticmethod
    def add_boxes(points, gt_boxes=None, ref_boxes=None, ref_labels=None, ref_scores=None, point_colors=None,
                  draw_origin=True, type='open3d'):
        if type == 'open3d':
            open3d_draw_scenes(
                points=points,
                gt_boxes=gt_boxes,
                ref_boxes=ref_boxes,
                ref_labels=ref_labels,
                ref_scores=ref_scores,
                point_colors=point_colors,
                draw_origin=draw_origin
            )
        elif type == 'opengl':
            pass
        elif type == 'mayavi':
            pass
        elif type == 'vispy':
            pass


if __name__ == '__main__':
    PointCloudProcess.show_pcd(path='D:/Code/wtao//000000.bin', pcd_range=[-10, -10, -5, 19.5, 10, 15])
