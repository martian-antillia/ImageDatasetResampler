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

# DatsetResampler.py

# 2022/08/12

# encodig: utf-8

import sys
import os
from absl import app

from absl import flags

import traceback
import shutil
import random
import tensorflow as tf
import glob

sys.path.append('../../')

from OfflineDataSetAugmentor import *


############################################################
#  
"""
Example: skin cancer HAM10000

skin cancer HAM10000/Training dataset
--------------------
class   num_images   
akiec   183          
bcc     266
bkl     564
df       56
mel     435
nv     3431
vasc     65
"""


FLAGS = flags.FLAGS

def define_flags():
  """Define all flags for binary run."""
  flags.DEFINE_string('image_size', '600x450', 'Image size (WIDTHxHEIGNT).')
  flags.DEFINE_string('data_dir', None, 'Locattion of orignal dataset images.')
  flags.DEFINE_string('resampled_dir',  None, 'Location of resampled dataset images')
  flags.DEFINE_string('strategy', None, 'Data resampling strateg')
  flags.DEFINE_integer('num_sample_images', None, 'Number of images of sampling.')



class DatasetReSampler:
  def __init__(self, strategy="CUSTOM_SAMPLIG", num_sample_images=130):
    self.strategy     = strategy
    self.UNDER_SAMPLING    = "UNDER_SAMPLING"
    self.MEAN_SAMPLING     = "MEAN_SAMPLING"
    self.OVER_SAMPLING     = "OVER_SAMPLING"
    self.CUSTOM_SAMPLING   = "CUSTOM_SAMPLING"
    self.image_format      = "jpg"
    self.RANDOM_SAMPLING   = 0
    self.COPY_ALL          = 1
    self.NEED_AUGMENTATION = 2
    self.NUM_SAMPLE_IMAGES = num_sample_images
    strategies = [self.UNDER_SAMPLING, 
                  self.MEAN_SAMPLING, 
                  self.OVER_SAMPLING, 
                  self.CUSTOM_SAMPLING]
    if not self.strategy in strategies:
      raise Exception("Invalid strategy {}".format(self.strategy)) 

  def copy_all(self, mini_dataset, augmented_dataset):
    print("---  OverSampler.copy_all() ")
    dataset_dir, load_format = mini_dataset
    save_dataset_dir, _     = augmented_dataset
    files = glob.glob(dataset_dir + "/*." + load_format)
    for i, file in enumerate(files):
      shutil.copy2(file, save_dataset_dir)
      print("--- copy2 from {} to {}".format(file, save_dataset_dir)) 

  def random_sampling(self, mini_dataset, augmented_dataset, n_samples):
    print("---  OverSampler.randoms_sampling() ")
    dataset_dir, load_format = mini_dataset
    save_dataset_dir, _      = augmented_dataset

    files = glob.glob(dataset_dir + "/*." + load_format)
    samples = random.sample(files, n_samples)
    for i, file in enumerate(samples):
      shutil.copy2(file, save_dataset_dir)
      print("--- copy2 from {} to {}".format(file, save_dataset_dir)) 


  def augmentation(self, sub_dataset, aug_sub_dataset, image_size, num_augmentation):     
    generator = tf.keras.preprocessing.image.ImageDataGenerator(
                                        rotation_range     = 20,    
                                        width_shift_range  = 0.2, #1.0, 
                                        height_shift_range = 0.2,
                                        shear_range        = 0.2,       
                                        zoom_range         = 0.2,        
                                        brightness_range   = [0.7,1.2],
                                        channel_shift_range= 2.0, 
                                        horizontal_flip    = True,
                                        vertical_flip      = True)     

    augmentor = OfflineDataSetAugmentor(generator = generator)
    augmentor.generate(sub_dataset, 
                           aug_sub_dataset, 
                           image_size = image_size,
                           n_augmentation=num_augmentation)

  def run(self, image_size       = (600, 450), 
                base_dataset_dir = "./HAM10000/Training",
                base_augment_dataset_dir  = "./OverSampling_HAM10000/Training"):
         
    labels = os.listdir(base_dataset_dir)
    labels = sorted(labels)
    print("--- labeles {}".format(labels))
    statistics = []
    SUM = 0
    MIN_NUM  = 10000
    MAX_NUM = 0
    for label in labels:
      subdir = os.path.join(base_dataset_dir, label)
      files  = glob.glob(subdir + "/*." + self.image_format)
      flen   = len(files)
      SUM += flen

      statistics.append((label, flen))
      if flen >= MAX_NUM:
        MAX_NUM = flen
      if flen <= MIN_NUM:
        MIN_NUM = flen

    print("--- file_statistis {}".format(statistics))
    
    num_labels = len(labels)
    MEAN_NUM = int(SUM/num_labels)
    print("--- MEAN_NUM {}".format(MEAN_NUM))
    augmentations = []

    for  item in statistics:
      label, num = item
      if self.strategy == self.UNDER_SAMPLING:
        print("--- UNDER_SAMPLLING ")
        self.NUM_SAMPLE_IMAGES = MIN_NUM
        augmentations.append((label, int(MIN_NUM/num)))

      elif self.strategy == self.MEAN_SAMPLING:
        self.NUM_SAMPLE_IMAGES = MEAN_NUM

        augmentations.append((label, int(MEAN_NUM/num)))

      elif self.strategy == self.OVER_SAMPLING:
        self.NUM_SAMPLE_IMAGES = MAX_NUM
        augmentations.append((label, int(MAX_NUM/num)))

      elif self.strategy == self.CUSTOM_SAMPLING:
        augmentations.append((label, int(self.NUM_SAMPLE_IMAGES/num)))

    print(augmentations)
    input("Hit any key")
    if not os.path.join(base_augment_dataset_dir):
      os.makedirs(base_augment_dataset_dir)

    for augmentation in augmentations:
      print("--- {}".format(augmentation))
      (label, num_augmentation) = augmentation
      # 1 Generate augmented images from mini_dataset,  and save them to augmented_dataset.
      sub_dataset_dir     = os.path.join(base_dataset_dir, label)
      aug_sub_dataset_dir = os.path.join(base_augment_dataset_dir, label)
      sub_dataset         = (sub_dataset_dir,     self.image_format)
      aug_sub_dataset     = (aug_sub_dataset_dir, self.image_format)

      if not os.path.exists(sub_dataset_dir):
        raise Exception("----Not found {}".format(sub_dataset_dir))
      if os.path.exists(aug_sub_dataset_dir):
        shutil.rmtree(aug_sub_dataset_dir)
        print("--- removed existing files {}".format(aug_sub_dataset_dir))
      if not os.path.exists(aug_sub_dataset_dir):
        os.makedirs(aug_sub_dataset_dir)
    
      if num_augmentation == self.RANDOM_SAMPLING:
        print("--- RANDOM_SAMPLING {}".format(num_augmentation))
        #input("HIT ANY KEY")
        self.random_sampling(sub_dataset, aug_sub_dataset, self.NUM_SAMPLE_IMAGES)
    
      elif num_augmentation == self.COPY_ALL:
        print("--- COPY ALL {}".format(num_augmentation))
        input("HIT ANY KEY")
        self.copy_all(sub_dataset, aug_sub_dataset)
        
      elif num_augmentation >= self.NEED_AUGMENTATION:
        print("--- NEED_AUGMENTATION {}".format(num_augmentation))
        input("HIT ANY KEY")
        self.augmentation(sub_dataset, aug_sub_dataset, image_size, num_augmentation)
      else:
        raise Exception("--- Invalid num_augmentation  " + str(num_augmentation))
 
      self.show_resampled_dataset(base_augment_dataset_dir)


  def show_resampled_dataset(self, dataset_dir):
    labels = os.listdir(dataset_dir)
    labels = sorted(labels)
    print("--- labeles {}".format(labels))
    statistics = []
    
    for label in labels:
      subdir = os.path.join(dataset_dir, label)
      files  = glob.glob(subdir + "/*.jpg")
      flen   = len(files)
      statistics.append((label, flen))
    print("--- file_statistis {}".format(statistics))


         
def main(_):
 
  try:
    image_size    = FLAGS.image_size
    w, h          = image_size.split("x")
    image_size    = (int(w), int(h))
    data_dir      = FLAGS.data_dir
    resampled_dir = FLAGS.resampled_dir
    strategy      = FLAGS.strategy
    num_sample_images = FLAGS.num_sample_images

    print("--- image_size   {}".format(image_size))
    print("--- base_images_dir {}".format(data_dir))
    print("--- aug_base_images_dir  {}".format(resampled_dir ))
    print("--- strategy {}".format(strategy))
    print("--- custom_max_num {}".format(num_sample_images))

    sampler = DatasetReSampler(strategy          = strategy, 
                               num_sample_images = num_sample_images)
    sampler.run(image_size, data_dir, resampled_dir)
    
  except:
    traceback.print_exc()

if __name__ == "__main__":
  define_flags()
  app.run(main)
