from __future__ import absolute_import, division, print_function

import os
import skimage.transform
import numpy as np
import PIL.Image as pil
from PIL import Image

from kitti_utils import generate_depth_map
from .mono_dataset import MonoDataset


class NCN_CH2_v4_Dataset(MonoDataset):
    """Superclass for different types of KITTI dataset loaders
    """
    def __init__(self, *args, **kwargs):
        super(NCN_CH2_v4_Dataset, self).__init__(*args, **kwargs)

        # NOTE: Make sure your intrinsics matrix is *normalized* by the original image size.
        # To normalize you need to scale the first row by 1 / image_width and the second row
        # by 1 / image_height. Monodepth2 assumes a principal point to be exactly centered.
        # If your principal point is far from the center you might need to disable the horizontal
        # flip augmentation.
        self.K = np.array([[0.65357, 0, 0.5, 0],
                           [0, 0.65357, 0.5, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype=np.float32)
        ##kitti_image_size
        ##self.full_res_shape = (1242, 375)
        ##ncn_ch2_size
        #self.full_res_shape = (1920, 1080)
        ##ncn_ch2_size
        #self.full_res_shape = (768, 256)
        ##ncn_ch2_resize
        ##self.full_res_shape = (1242, 376)
        ##ncn_ch2_crop_v2
        self.full_res_shape = (1500, 454)


        
        ## 스테리오 카메라 정보
        #self.side_map = {"2": 2, "3": 3, "l": 2, "r": 3}

        
    def check_depth(self):
        # We don't have depth data
        return False
    
    
    def get_color(self, folder, frame_index, side, do_flip):
        #color = self.loader(self.get_image_path(folder, frame_index, side))


        image_path = self.get_image_path(folder, frame_index, side)
        color = self.loader(image_path)

        if do_flip:
            color = color.transpose(pil.FLIP_LEFT_RIGHT)

        return color

    def get_image_path(self, folder, frame_index, side):
        # f_str = "{:010d}{}".format(frame_index, self.img_ext)
        f_str = "{:010}{}".format(frame_index, self.img_ext) # for ai-hub data


        # image_path = os.path.join(
        #     # 폴더 경로 == <data_path>/<folder>/{:010d}.jpg
        #     # ex) ./train_data/frames/lozan/00000000001.jpg
        #     self.data_path, folder, 'image_00', 'data', f_str)
        # return image_path

        # image_path = os.path.join(
        #     # 폴더 경로 == <data_path>/<folder>/{:010d}.jpg
        #     # ex) ./train_data/frames/lozan/00000000001.jpg
        #     self.data_path, folder, f_str) # for ai-hub data
        
        for sub_folder in os.listdir(self.data_path):
            # 이미지 경로 생성
            image_path = os.path.join(self.data_path, sub_folder, f_str)
            if os.path.isfile(image_path):
                return image_path
        return image_path

    
    


