rem 1_train_dataset_resampler.bat
python ../../DatasetResampler.py ^
  --image_size=600x450 ^
  --data_dir=./HAM10000/Training  ^
  --resampled_dir=./Resampled_HAM10000-700/Training ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=700 ^
  --debug=False


