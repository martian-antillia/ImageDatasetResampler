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

from ConfigParser  import ConfigParser
from OfflineDataSetAugmentor import *


############################################################
#  
"""
Example: skin cancer HAM10000

skin cancer HAM10000/PARAMETERS dataset
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
  flags.DEFINE_string('data_generator_config', None, 'Path to an image augmentation configuration file.')

  flags.DEFINE_string('image_size', '600x450', 'Image size (WIDTHxHEIGNT).')

  flags.DEFINE_string('data_dir', None, 'Locattion of orignal dataset images.')
  flags.DEFINE_string('resampled_dir',  None, 'Location of resampled dataset images')
  flags.DEFINE_string('strategy', None, 'Data resampling strategy')
  flags.DEFINE_integer('num_sample_images', None, 'Number of images of sampling.')
  flags.DEFINE_boolean('debug', False, 'Debug flag')


class DatasetReSampler:
  def __init__(self, 
               strategy="CUSTOM_SAMPLIG", 
               num_sample_images=130,
               data_generator_config=None):
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
    self.data_generator_config = data_generator_config

  def copy_all(self, mini_dataset, augmented_dataset):
    #print("---  copy_all() ")
    dataset_dir, load_format = mini_dataset
    save_dataset_dir, _     = augmented_dataset
    files = glob.glob(dataset_dir + "/*." + load_format)
    for i, file in enumerate(files):
      shutil.copy2(file, save_dataset_dir)
      if FLAGS.debug:
        print("--- copy2 from {} to {}".format(file, save_dataset_dir)) 

  def random_sampling(self, mini_dataset, augmented_dataset, n_samples):
    #print("---  randoms_sampling() ")
    dataset_dir, load_format = mini_dataset
    save_dataset_dir, _      = augmented_dataset

    files = glob.glob(dataset_dir + "/*." + load_format)
    samples = random.sample(files, n_samples)
    for i, file in enumerate(samples):
      shutil.copy2(file, save_dataset_dir)
      if FLAGS.debug:
        print("--- copy2 from {} to {}".format(file, save_dataset_dir)) 


  def augmentation(self, sub_dataset, aug_sub_dataset, image_size, num_augmentation):
    if self.data_generator_config != None:
      parser = ConfigParser(self.data_generator_config)
      PARAMETERS = "parameters"
      generator = tf.keras.preprocessing.image.ImageDataGenerator(
          featurewise_center              = parser.get(PARAMETERS, "featurewise_center", False),
          samplewise_center               = parser.get(PARAMETERS, "samplewise_center",  False),
          featurewise_std_normalization   = parser.get(PARAMETERS, "featurewise_std_normalization", False),
          samplewise_std_normalization    = parser.get(PARAMETERS, "samplewise_std_normalization", False),
          zca_whitening                   = parser.get(PARAMETERS, "zca_whitening",                False),
   
          rotation_range                  = parser.get(PARAMETERS, "rotation_range", 8),
          horizontal_flip                 = parser.get(PARAMETERS, "horizontal_flip", True),
          vertical_flip                   = parser.get(PARAMETERS, "vertical_flip", True),

          width_shift_range               = parser.get(PARAMETERS, "width_shift_range", 0.9), 
          height_shift_range              = parser.get(PARAMETERS, "height_shift_range", 0.9),
          shear_range                     = parser.get(PARAMETERS, "shear_range", 0.1), 
          zoom_range                      = parser.get(PARAMETERS, "zoom_range", 0.1), 
          #zoom_range         = [0.8, 1.2],
          )
    else: 
      generator = tf.keras.preprocessing.image.ImageDataGenerator(
                                        featurewise_center = True,
                                        samplewise_center  = False,
                                        featurewise_std_normalization=True,
                                        samplewise_std_normalization =False,

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

  # Skin Cancer HAM10000
  def run(self, image_size       = (600, 450), 
                base_dataset_dir = "./HAM10000/PARAMETERS",
                base_augment_dataset_dir  = "./OverSampling_HAM10000/PARAMETERS"):
         
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
    print("\n--- Original dataset")
    print("--- statistics:\n{}".format(statistics))
    
    num_labels = len(labels)
    MEAN_NUM = int(SUM/num_labels)
    #print("--- MEAN_NUM {}".format(MEAN_NUM))
    augmentations = []

    for  item in statistics:
      label, num = item
      if self.strategy == self.UNDER_SAMPLING:
        #print("--- UNDER_SAMPLLING ")
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
    if FLAGS.debug:
      print("--- Resampling parameter")
      print(augmentations)
    #input("Hit any key")
    if not os.path.join(base_augment_dataset_dir):
      os.makedirs(base_augment_dataset_dir)

    for augmentation in augmentations:
      #print("--- {}".format(augmentation))
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
        #print("--- removed existing files {}".format(aug_sub_dataset_dir))
      if not os.path.exists(aug_sub_dataset_dir):
        os.makedirs(aug_sub_dataset_dir)
    
      if num_augmentation == self.RANDOM_SAMPLING:
        #print("--- RANDOM_SAMPLING {}".format(num_augmentation))
        #input("HIT ANY KEY")
        self.random_sampling(sub_dataset, aug_sub_dataset, self.NUM_SAMPLE_IMAGES)
    
      elif num_augmentation == self.COPY_ALL:
        #print("--- COPY ALL {}".format(num_augmentation))
        #input("HIT ANY KEY")
        self.copy_all(sub_dataset, aug_sub_dataset)
        
      elif num_augmentation >= self.NEED_AUGMENTATION:
        #print("--- NEED_AUGMENTATION {}".format(num_augmentation))
        #input("HIT ANY KEY")
        self.augmentation(sub_dataset, aug_sub_dataset, image_size, num_augmentation)
      else:
        raise Exception("--- Invalid num_augmentation  " + str(num_augmentation))

    self.show_dataset_statistics(base_dataset_dir)

    self.show_dataset_statistics(base_augment_dataset_dir)


  def show_dataset_statistics(self, dataset_dir):
    print("\n--- Resampled dataset")
    labels = os.listdir(dataset_dir)
    labels = sorted(labels)
    #print("--- labeles {}".format(labels))
    statistics = []
    
    for label in labels:
      subdir = os.path.join(dataset_dir, label)
      files  = glob.glob(subdir + "/*.jpg")
      flen   = len(files)
      statistics.append((label, flen))
    print("--- statistics:\n{}".format(statistics))


         
def main(_):
 
  try:
    image_size    = FLAGS.image_size
    w, h          = image_size.split("x")
    image_size    = (int(w), int(h))
    data_dir      = FLAGS.data_dir
    resampled_dir = FLAGS.resampled_dir
    strategy      = FLAGS.strategy
    num_sample_images = FLAGS.num_sample_images
    data_generator_config = FLAGS.data_generator_config

    print("--- image_size     {}".format(image_size))
    print("--- dataset_dir    {}".format(data_dir))
    print("--- resampled_dir  {}".format(resampled_dir ))
    print("--- strategy       {}".format(strategy))
    print("--- data_generator_config       {}".format(data_generator_config))
    if not os.path.exists(data_generator_config):
      raise Exception("Not found " + data_generator_config)

    sampler = DatasetReSampler(strategy          = strategy, 
                               num_sample_images = num_sample_images,
                               data_generator_config = data_generator_config)
    sampler.run(image_size, data_dir, resampled_dir)
    
  except:
    traceback.print_exc()

if __name__ == "__main__":
  define_flags()
  app.run(main)
