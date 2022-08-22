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

#  OpenCVCroppedImageReader.py


# encoding: utf-8

import sys
import os
import traceback


import cv2
sys.path.append("../../")

from OpenCVImageReader       import *

class OpenCVCroppedImageReader(OpenCVImageReader):

  def __init__(self, to_rgb = True):
    super(OpenCVCroppedImageReader, self).__init__(to_rgb)


  def crop_max_square_region(self, image, scale=None, debug=False):
    h, w = image.shape[:2]
    if debug:
      print ("w:" + str(w) + " h:" + str(h))
    
    # Get a size of a maximum square region of the image 
    if w > h:
      s = h
    else:
      s = w
    y = int( (h - s)/2 )
    x = int( (w - s)/2 )

    cropped = image[y:y+s, x:x+s]

    if scale != None:
       cropped  = cv2.resize(cropped, dsize=scale)

    return cropped


