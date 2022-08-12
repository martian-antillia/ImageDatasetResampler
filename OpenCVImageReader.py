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

#  OpenCVImageReader.py


# encoding: utf-8

import sys
import os
import traceback

# We use OpenCV-4.0.X library

import cv2
sys.path.append("../../")

class OpenCVImageReader:

  def __init__(self, to_rgb = True):
    # Flag to convert bgr to rgb.
    self.bgr_to_rgb = to_rgb
    
  def read(self, filename="", flag=cv2.IMREAD_COLOR):
    abspath = os.path.abspath(filename)
    print("abspath:{}".format(abspath))
   
    if not os.path.isfile(abspath):
      raise FileNotFoundError(errno.ENOENT, 
              os.strerror(errno.ENOENT), abspath)

    image = cv2.imread(abspath, flag)
    if self.bgr_to_rgb == True:
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

