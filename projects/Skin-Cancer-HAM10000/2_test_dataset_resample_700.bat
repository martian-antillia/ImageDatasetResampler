rem 2_test_dataset_resampler.bat
python ../../DatasetReSampler.py ^
  --image_size=600x450 ^
  --data_dir=./HAM10000/Testing  ^
  --resampled_dir=./Resampled_HAM10000-700/Testing ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=200



