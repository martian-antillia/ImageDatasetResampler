<h2>
ImageDatasetResampler (Updated: 2022/08/22)
</h2>
This is a simple <b>Image Dataset Resampling Tool</b> to resample original
image dataset, which supports the following strategies:<br>
UNDER_SAMPLING,<br>
MEAN_SAMPLING,<br> 
OVER_SAMPLING,<br> 
CUSTOM_SAMPLING.<br>
<br>
This tool will be helpful to generate a balanced dataset from an imbalanced image dataset by our resampling strategies.<br><br> 
We use Python 3.8 and Tensorflow 2.8.0 environment on Windows 11.
<br>
In cases of MEAN, OVER and CUSTOM SAMPLING, we use <a href="./OfflineDataSetAugmentor.py">OfflineDataSetAugmentor</a> class, in which
<pre>
tf.keras.preprocessing.image.ImageDataGenerator
</pre>
is used to augment the images in minority classes.<br>
<br>
<li>
2022/08/21: Modified to reset radom_seeds, and to use a seed parameter 
 in generate method of OfflineDatasetAugmentor class.
</li>
<li>
2022/08/22: Added <a href="./SquareRegionImageCropper.py">SquareRegionImageCropper</a> class to crop maximum square region from the original images.
</li>
<li>
2022/08/22: Added a script file to create <b>Cropped_HAM10000</b> dataset, and <b>Cropped_Resampled_HAM10000_300</b> dataset.
</li>

<br>
<h2>
1 Project 
</h2>
<h3>
1.1 Skin-Cancer-HAM10000
</h3>
The dataset <b>Skin-Cancer-HAM10000</b> has been taken from the following web site:

The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions

Harvard edu dataset:

 https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T


HAM10000 folder has Testing and Training subfolders, and they have classified subfolders
of akiec, bcc, bkl, df, mel, nv, and vasc as shown below:

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
Training dataset has been reconstructed from <br>
  <b>HAM10000_images_part_1.zip and HAM10000_metadata.tab</b> in Harvard edu dataset above:
<br>

Testing dataset has been reconstructed from <br>
  <b>HAM10000_images_part_2.zip and HAM10000_metadata.tab</b> in Harvard edu dataset above:
<br>

<h3>
1.2 Resampling Skin-Cancer-HAM10000
</h3>
As you may know, Skin-Cancer-HAM10000 dataset is a typical imbalanced dataset, so we would like to create to a balanced dataset
by resampling images from the orginal HAM10000 dataset.
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
  --data_generator_config=./data_generator.config ^
  --image_size=600x450 ^
  --data_dir=./HAM10000/Training  ^
  --resampled_dir=./Resampled_HAM10000/Training ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=100
</pre>
Console output:<br>
<img src="./asset/train_dataset_resampling.png"  with="720" height="auto">
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
  --data_generator_config=./data_generator.config ^
  --image_size=600x450 ^
  --data_dir=./HAM10000/Testing  ^
  --resampled_dir=./Resampled_HAM10000/Testing ^
  --strategy=UNDER_SAMPLING 
</pre>
Console output:<br>
<img src="./asset/test_dataset_resampling.png" with="720" height="auto">


<h3>
1.2.3 Download Resampled_HAM10000
</h3>
You can download the generated <b>Skin Cancer Resampled_HAM10000</b> dataset from the following google drive:<br>
 <a href="https://drive.google.com/file/d/1OqRiuFArflpw-8Anm2UV4EdyfS77ANTA/view?usp=sharing">Resampled_HAM10000.zip</a>

<!--
  -->
<h3>
1.3 Apply SquareRegionImageCropper to HAM10000
</h3>
You can generate Square-Region-Cropped HAM10000 dataset from Skin-Cancer-HAM10000 dataset by using
<a href="./SquareRegionImageCropper.py">SquareRegionImageCropper</a>.
<br>
<h3>
1.3.1 ImageSquareRegionCropper
</h3>
Run the following command to create Cropped_HAM10000 dataset from the original HAM10000:<br>
<pre>
./0_create_cropped_image_dataset.bat
</pre>
<pre>
rem 0_create_cropped_image_dataset.bat
python ../../SquareRegionImageCropper.py ^
  ./HAM10000/Training ^
  ./Cropped_HAM10000/Training
  
python ../../SquareRegionImageCropper.py ^
  ./HAM10000/Testing ^
  ./Cropped_HAM10000/Testing</pre>
Console output:<br>
<img src="./asset/create_cropped_image_dataset.png" with="720" height="auto">
<br>
<br>
This scripts will generate the cropped images of square region size (450, 450) from original images of size (600, 450) in HAM10000.
<br>

<h3>
1.4 Resampling Cropped_HAM10000 dataset
</h3>

<h3>1.4.1 Resampling training dataset
</h3>
Run the following command to generate Cropped_Resampled_HAM10000_300/Training dataset:<br>
<pre>
./1_cropped_train_dataset_resampler_300.bat
</pre>
<pre>
rem 1_cropped_train_dataset_resampler_300.bat
python ../../DatasetResampler.py ^
  --data_generator_config=./data_generator.config ^
  --image_size=450x450 ^
  --data_dir=./Cropped_HAM10000/Training  ^
  --resampled_dir=./Cropped_Resampled_HAM10000_300/Training ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=300
</pre>
Console output:<br>
<img src="./asset/cropped_train_dataset_resampler_300.png" with="720" height="auto">


<h3>1.4.2 Resampling testing dataset
</h3>
Run the following command to generate Cropped_Resampled_HAM10000_300/Testing dataset:<br>
<pre>
./2_cropped_test_dataset_resampler_300.bat
</pre>
<pre>
rem 2_cropped_test_dataset_resampler_300.bat
python ../../DatasetReSampler.py ^
  --data_generator_config=./data_generator.config ^
  --image_size=450x450 ^
  --data_dir=./Cropped_HAM10000/Testing  ^
  --resampled_dir=./Cropped_Resampled_HAM10000_300/Testing ^
  --strategy=CUSTOM_SAMPLING ^
  --num_sample_images=100
</pre>
Console output:<br>
<img src="./asset/cropped_test_dataset_resampler_300.png" with="720" height="auto">




