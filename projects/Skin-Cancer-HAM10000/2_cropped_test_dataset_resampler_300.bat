rem 2_cropped_test_dataset_resampler_300.bat
python ../../DatasetReSampler.py ^
  --data_generator_config=./data_generator.config ^
  --image_size=450x450 ^
  --image_format=jpg ^
  --data_dir=./Cropped_HAM10000/Testing  ^
  --resampled_dir=./Cropped_Resampled_HAM10000_300/Testing ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=100
