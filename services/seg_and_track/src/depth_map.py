import cv2.aruco as aruco
import numpy as np
import torch
import os
import cv2
import matplotlib.pyplot as plt
from copy import deepcopy
from huggingface_hub import hf_hub_download
from .metric_depth.depth_anything_v2.dpt import DepthAnythingV2
from sklearn.linear_model import RANSACRegressor, LinearRegression


class DepthEvaluator:
    def __init__(self, device: str):
        model_path_hg = hf_hub_download(
            repo_id="depth-anything/Depth-Anything-V2-Metric-Hypersim-Base",
            filename="depth_anything_v2_metric_hypersim_vitb.pth",
        )
        params = {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]}
        self.model = DepthAnythingV2(**params, max_depth=20.0)
        self.model.load_state_dict(torch.load(model_path_hg))
        self.model.to(device)

    def get_depth_map(
        self,
        img: np.ndarray,
        aruco_dict: aruco.Dictionary,
        parameters: aruco.DetectorParameters,
        camera_matrix: np.ndarray,
        distortion_coeffs: np.ndarray,
        save_path: str = None,
        visualize: bool = False,
    ) -> np.ndarray:
        """
        Calibrated Depth Anything V2 depth map using distances to aruco markers and returns depth map of an image

        Note:
            Depth map will be in the same units as camera_matrix

        Args:
            img: image
            aruco_dict: aruco dictionary
            parameters: aruco detected parameters
            camera_matrix: camera matrix
            distortion_coeffs: distortion coefficients of a camera
            save_path: path to save a depth map, None if dont save
            visualize: whether visualize depth map or not

        Returns
            Depth map
        """
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Model inference
        depth = self.model.infer_image(img)
        # Getting distance from camera to aruco markers
        corners, ids, rej = aruco.detectMarkers(img_gray, aruco_dict, parameters=parameters)
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.08, camera_matrix, distortion_coeffs)
        z_vals = []
        depth_vals = []
        if tvec is not None:
            for ind, cur_tvec in enumerate(tvec):
                z = np.linalg.norm(cur_tvec[0])  # getting z coordinate, abs just in case
                corner = corners[ind][0]
                tl, br = corner[0], corner[2]
                center = (int((tl[1] + br[1]) / 2), int((tl[0] + br[0]) / 2))
                z_vals.append(z)
                depth_vals.append([depth[center[0]][center[1]]])

        # Scaling the depth map
        if len(z_vals) == 0:
            pass
        elif len(z_vals) == 1:
            depth = depth * (z_vals[0] / depth_vals[0])
        else:
            lin = LinearRegression()
            lin.fit(X=depth_vals, y=z_vals)
            if lin.coef_[0] < 0:
                depth = depth * np.mean([z_ / depth_ for z_, depth_ in zip(z_vals, depth_vals)])
            else:
                depth = depth * lin.coef_[0] + lin.intercept_

        if save_path:
            np.save(os.path.join(save_path), depth)
        if visualize:
            plt.imshow(depth)
            plt.colorbar()
            plt.show()

        return depth


class PlaneDetector:
    def __init__(self, camera_matrix: np.ndarray):
        self.camera_matrix = camera_matrix

    def get_point_cloud(self, depth_map: np.ndarray) -> np.ndarray:
        """
        Returns point cloud of an image

        Args:
            depth_map: a depth map of an image in target units
            focal_length: focal length of a camera in meters

        Returns:
            Stacked real x, y and z coordinates
        """
        h, w = depth_map.shape
        x, y = np.meshgrid(np.arange(w), np.arange(h))
        u = (x - self.camera_matrix[0][2]) / self.camera_matrix[0, 0]
        v = (y - self.camera_matrix[1][2]) / self.camera_matrix[1, 1]
        cos_angels = 1 / np.sqrt(u ** 2 + v ** 2 + 1)
        z = np.multiply(cos_angels, depth_map)
        point_cloud = np.stack(
            (np.multiply(u, z), np.multiply(v, z), z)  # 3, h, w
        )
        return point_cloud

    def get_plane_size(
        self, point_cloud: np.ndarray, mask: np.ndarray, threshold: float = None, img: np.ndarray = None
    ) -> tuple[float, float]:
        """
        Detects a plane and returns its real world size

        Args:
            point_cloud: stacked real x, y and z coordinates
            mask: region of interest where to search for plane
            threshold: max absolute difference from plane so that the point is considered in that plane
            img: initial image (only for visualization purposes)

        Returns
            Width and height
        """
        # Detecting a plane
        mask = mask.astype(bool)
        x_real, y_real, z_real = point_cloud[0][mask], point_cloud[1][mask], point_cloud[2][mask]
        ransac = RANSACRegressor(residual_threshold=threshold, min_samples=3, random_state=42)
        ransac.fit(np.stack((x_real, y_real), axis=1), z_real)
        mask_indices = np.stack((np.where(mask == 1)[0], np.where(mask == 1)[1]), axis=1)
        inliers_points = mask_indices[ransac.inlier_mask_]
        # Visualization
        if img is not None:
            img_copy = deepcopy(img)
            for point in inliers_points:
                img_copy[point[0]][point[1]] = (255, 0, 0)
            plt.imshow(img_copy)
            plt.show()
        # Size calculation
        points_3d = np.stack(
            [x_real[ransac.inlier_mask_], y_real[ransac.inlier_mask_], z_real[ransac.inlier_mask_]], axis=-1
        )

        width = points_3d[:, 0].max() - points_3d[:, 0].min()
        height = points_3d[:, 1].max() - points_3d[:, 1].min()

        return width, height
