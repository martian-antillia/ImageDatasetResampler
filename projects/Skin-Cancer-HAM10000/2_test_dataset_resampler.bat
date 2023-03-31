rem 2_test_dataset_resampler.bat
python ../../DatasetReSampler.py ^
  --data_generator_config=./data_generator.config ^
  --image_size=600x450 ^
  --image_format=jpg ^
  --data_dir=./HAM10000/Testing  ^
  --resampled_dir=./Resampled_HAM10000/Testing ^
  --strategy=UNDER_SAMPLING 


