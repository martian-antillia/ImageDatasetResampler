rem 1_train_dataset_resampler_500.bat
python ../../DatasetResampler.py ^
  --data_generator_config=./data_generator.config ^
  --image_size=600x450 ^
  --data_dir=./HAM10000/Training  ^
  --resampled_dir=./Resampled_HAM10000-500/Training ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=500 ^
  --debug=False


