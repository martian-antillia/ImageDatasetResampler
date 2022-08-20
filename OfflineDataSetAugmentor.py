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

#  OfflineDataSetAugmentor.py

# This class generates and saves images to generate a augmented-dataset from a mini-dataset
# by using Keras ImageDataGenerator.
 

# 2022/08/09


# encodig: utf-8

import sys
import os
import traceback
import glob
import shutil
import random

sys.path.append("../../")

from OpenCVCroppedImageReader import OpenCVCroppedImageReader
import tensorflow as tf

class OfflineDataSetAugmentor:
  ##
  # Constructor
  def __init__(self, generator=None):
    
    self.generator = generator
    if self.generator == None:
      # Create a default instance of ImageDataGenerator
      self.generator = tf.keras.preprocessing.image.ImageDataGenerator(
      
                                        rotation_range     = 20,    
                                        width_shift_range  = 1.0, 
                                        height_shift_range = 0.3,
                                        shear_range        = 0.4,       
                                        zoom_range         = 0.3,        
                                        brightness_range   = [0.7,1.2],
                                        channel_shift_range= 2.0, 
                                        horizontal_flip    = True,
                                        vertical_flip      = False)                                      
      

  # The parameters mini_dataset and augmented_dataset 
  # will take a tuple (dataset_folder, image_format) respectively
  def generate(self, 
              mini_dataset, 
              augmented_dataset, 
              image_size     =(128, 128), 
              n_augmentation = 1000,
              seed           = 123):
  
    print("--- OfflineDataSetAugmentor.generate()")

    self.mini_dataset_folder, self.load_format = mini_dataset
  
    self.save_dataset_folder, self.save_format = augmented_dataset


    self.size        = image_size
    print("--- self.size {}".format(self.size))
    #subfolders = sorted( os.listdir(self.mini_dataset_folder) )
    print("--- base mini_dataset_folder {}".format(self.mini_dataset_folder))

    #for index, folder in enumerate(subfolders):
    dir = self.mini_dataset_folder # os.path.join(self.mini_dataset_folder, folder)
    #print("dir " + dir)

    files = glob.glob(dir + "/*." + self.load_format)
    for i, file in enumerate(files):
        try:
        
          # Get an image cropped with max square region and scaled with self.size
          reader  = OpenCVCroppedImageReader()
          image   = reader.read(file)
          image   = reader.crop_max_square_region(image, self.size)

          #  Reshape the image from (height, width, channles) to (1, height, width, channels)
          self.data = image.reshape((1,) + image.shape)

          save_folder = self.save_dataset_folder
          #print(save_folder)
          if not os.path.exists(save_folder):
             os.makedirs(save_folder)
          
          basename = os.path.basename(file)
          name     = basename.split(".")[0]
          #  Get a flow from the self.generator
          flow  = self.generator.flow(self.data, batch_size=1, 
                      save_to_dir = save_folder,
                      save_prefix = name, 
                      save_format =  self.save_format,
                      seed        = seed)

          # Get generated images from the flow, and save them to the save_folder  
          for i in range(n_augmentation):
            print(str(i) + " Saving a generated image to :" + save_folder)

            # Get a generated image from the flow, which is saved automatically.
            batches = next(flow)

        except:
          traceback.print_exc()


