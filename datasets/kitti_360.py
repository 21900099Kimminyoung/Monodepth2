from __future__ import absolute_import, division, print_function

import os
import skimage.transform
import numpy as np
import PIL.Image as pil

from kitti_utils import generate_depth_map
from .mono_dataset import MonoDataset


class KITTI360(MonoDataset):
    """Superclass for different types of KITTI dataset loaders
    """
    def __init__(self, *args, **kwargs):
        super(KITTI360, self).__init__(*args, **kwargs)

        # NOTE: Make sure your intrinsics matrix is *normalized* by the original image size.
        # To normalize you need to scale the first row by 1 / image_width and the second row
        # by 1 / image_height. Monodepth2 assumes a principal point to be exactly centered.
        # If your principal point is far from the center you might need to disable the horizontal
        # flip augmentation.


        '''
        %YAML:1.0
        model_type: MEI
        camera_name: image_02
        image_width: 1400
        image_height: 1400
        mirror_parameters:
            xi: 2.2134047507854890e+00
        distortion_parameters:
            k1: 1.6798235660113681e-02
            k2: 1.6548773243373522e+00
            p1: 4.2223943394772046e-04
            p2: 4.2462134260997584e-04
        projection_parameters:
            gamma1: 1.3363220825849971e+03
            gamma2: 1.3357883350012958e+03
            u0: 7.1694323510126321e+02
            v0: 7.0576498308221585e+02
        '''

        # 카메라 모델이 다르다??
        # https://github.com/autonomousvision/kitti360Scripts/issues/79
        
        self.K = np.array([[0.58, 0, 7.1694323510126321e+02 / 1400, 0],
                           [0, 1.92, 7.0576498308221585e+02 / 1400, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype=np.float32)

        self.full_res_shape = (1400, 1400)
        self.side_map = {"2": 2, "3": 3, "l": 2, "r": 3}

    def get_color(self, folder, frame_index, side, do_flip):
        color = self.loader(self.get_image_path(folder, frame_index, side))

        if do_flip:
            color = color.transpose(pil.FLIP_LEFT_RIGHT)

        return color
    
    def get_image_path(self, folder, frame_index, side):
        f_str = "{:010d}{}".format(frame_index, self.img_ext)
        image_path = os.path.join(
            self.data_path, folder, "image_0{}/data".format(self.side_map[side]), f_str)
        return image_path
    
    def check_depth(self):
        # We don't have depth data
        return False
    
    def get_depth(self, folder, frame_index, side, do_flip):
        print("get_depth: This function should not be called!") # because we don't have depth data
        return None