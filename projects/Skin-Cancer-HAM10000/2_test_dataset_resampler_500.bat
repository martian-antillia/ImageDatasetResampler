rem 2_test_dataset_resampler.bat
python ../../DatasetReSampler.py ^
  --data_generator_config=./data_generator.config ^
  --image_size=600x450 ^
  --data_dir=./HAM10000/Testing  ^
  --resampled_dir=./Resampled_HAM10000-500/Testing ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=150



