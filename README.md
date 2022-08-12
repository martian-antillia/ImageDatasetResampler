<h2>
ImageDatasetResampler (Updated: 2022/08/12)
</h2>
This is a simple Image Dataset Resampling Tool to resample original
image dataset, which supports the following strategies:<br>
Under_Sampling,<br>
Mean_Sampling,<br> 
Over_Sampling,<br> 
Custom_Sampling.<br>
<br>
We use Python 3.8 and Tensorflow 2.8.0 environment on Windows 11.
<br>
<h2>
1 Project 
</h2>
<h3>
1.1 Skin-Canncer-HAM10000
</h3>
The dataset <b>Skin-Canncer-HAM10000</b> has been taken from the following web site:

The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions

Harvard edu dataset:

 https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T


HAM10000 folder has Testing and Training subfolders, and they have classified subfolders
of akiec, bcc, bkl, df, mel, nv, vasc.

<pre>
HAM10000
├─Testing
│  ├─akiec
│  ├─bcc
│  ├─bkl
│  ├─df
│  ├─mel
│  ├─nv
│  └─vasc
└─Training
    ├─akiec
    ├─bcc
    ├─bkl
    ├─df
    ├─mel
    ├─nv
    └─vasc
</pre>
Training dataset has been reconstructed from 
  HAM10000_images_part_1.zip and HAM10000_metadata.tab in Harvard edu dataset above:


Training dataset has been reconstructed from 
  HAM10000_images_part_2.zip and HAM10000_metadata.tab in Harvard edu dataset above:


<h3>
1.2 Resampling Skin-Canncer-HAM10000
</h3>
Skin-Canncer-HAM10000 dataset is a typical imbalanced dataset.
<br>
<h3>
1.2.1 Resampling training dataset
</h3>
Run the following command:<br>
<pre>
./1_train_dataset_resampler.bat
</pre>
<pre>
rem 1_train_dataset_resampler.bat
python ../../DatasetSampler.py ^
  --image_size=600x450 ^
  --data_dir=./HAM10000/Training  ^
  --resampled_dir=./Resampled_HAM10000/Training ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=100
</pre>
Console output:<br>
<img src="./asset/train_dataset_resampling.png">
<br>
<h3>
1.2.2 Resampling tesing dataset
</h3>
Run the following command:<br>
<pre>
./2_test_dataset_resampler.bat
</pre>
<pre>
rem 2_test_dataset_resampler.bat
python ../../DatasetReSampler.py ^
  --image_size=600x450 ^
  --data_dir=./HAM10000/Testing  ^
  --resampled_dir=./Resampled_HAM10000/Testing ^
  --strategy=UNDER_SAMPLING 
</pre>
Console output:<br>
<img src="./asset/test_dataset_resampling.png">