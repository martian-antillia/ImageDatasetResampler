rem 1_cropped_train_dataset_resampler_300.bat
python ../../DatasetResampler.py ^
  --data_generator_config=./data_generator.config ^
  --image_size=450x450 ^
  --image_format=jpg ^
  --data_dir=./Cropped_HAM10000/Training  ^
  --resampled_dir=./Cropped_Resampled_HAM10000_300/Training ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=300

