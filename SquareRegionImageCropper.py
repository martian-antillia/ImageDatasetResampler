# Copyright 2022 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ImageSqureRegionCropper.py

# 2022/08/22

# encodig: utf-8

import sys
import os
#https://github.com/NVIDIA/framework-determinism/blob/master/doc/tensorflow.md
os.environ['PYTHONHASHSEED'] = '0'
#os.environ['TF_DETERMINISTIC_OPS'] = 'true'
os.environ['TF_CUDNN_DETERMINISTIC'] = 'true'

from absl import app

from absl import flags
import numpy as np
import traceback
import shutil
import random
import cv2

#import tensorflow as tf
import glob


sys.path.append('../../')

from OpenCVCroppedImageReader import OpenCVCroppedImageReader 

############################################################
#  
# Skin-Cancer-HAM10000
# image size = 600,450

class ImageSquareRegionCropper:
  def __init__(self):
    pass
  # Skin Cancer HAM10000
  def run(self, 
                dataset_dir = "./HAM10000/",
                cropped_dataset_dir  = "./Cropped_HAM10000/",
                debug = False):
         
    labels = os.listdir(dataset_dir)
    labels = sorted(labels)

    print("--- labeles {}".format(labels))
    image_reader = OpenCVCroppedImageReader(to_rgb=False)

    for label in labels:
      #print("--- {}".format(augmentation))
      # 1 Generate augmented images from mini_dataset,  and save them to augmented_dataset.
      sub_dataset_dir     = os.path.join(dataset_dir, label)
      cropped_sub_dataset_dir = os.path.join(cropped_dataset_dir, label)
   
      if not os.path.exists(sub_dataset_dir):
        raise Exception("----Not found {}".format(sub_dataset_dir))
      if os.path.exists(cropped_sub_dataset_dir):
        shutil.rmtree(cropped_sub_dataset_dir)
        #print("--- removed existing files {}".format(aug_sub_dataset_dir))
      if not os.path.exists(cropped_sub_dataset_dir):
        os.makedirs(cropped_sub_dataset_dir)
    
      files = glob.glob(sub_dataset_dir + "/*.jpg")
      for file in files:
        image = cv2.imread(file)
        h, w = image.shape[:2]
        if debug:
          print ("--- original_image shape w:" + str(w) + " h:" + str(h))

        cropped_image = image_reader.crop_max_square_region(image)
        basename = os.path.basename(file)
        cropped_image_file = os.path.join(cropped_sub_dataset_dir, basename)
        #BGR cv2 format
        h, w = cropped_image.shape[:2]
        if debug:
          print ("--- cropped_image shape w:" + str(w) + " h:" + str(h))

        cv2.imwrite(cropped_image_file, cropped_image)
         

def main(_): 
  try:
    if len(sys.argv) == 3:
      data_dir      = sys.argv[1]
      cropped_data_dir = sys.argv[2]
    else:
      raise Exception("Error: Invalid argment")
    if not os.path.exists(data_dir):
      raise Exception("Invalid data_dir " + data_dir)
    image_cropper = ImageSquareRegionCropper()
    image_cropper.run(data_dir, cropped_data_dir)
    
  except:
    traceback.print_exc()

if __name__ == "__main__":
  app.run(main)
