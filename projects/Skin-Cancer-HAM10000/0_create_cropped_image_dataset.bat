rem 0_create_cropped_image_dataset.bat
python ../../SquareRegionImageCropper.py ^
  ./HAM10000/Training ^
  ./Cropped_HAM10000/Training
  
python ../../SquareRegionImageCropper.py ^
  ./HAM10000/Testing ^
  ./Cropped_HAM10000/Testing
 