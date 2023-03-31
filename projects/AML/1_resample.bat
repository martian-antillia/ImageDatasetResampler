rem 1_train_dataset_resampler.bat
python ../../DatasetResampler.py ^
  --data_generator_config=./data_generator.config ^
  --image_size=360x360 ^
  --image_format=tiff ^
  --data_dir=./AML-Cytomorphology  ^
  --resampled_dir=./Resampled_AML-Cytomorphology_2000_360x360 ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=2000

