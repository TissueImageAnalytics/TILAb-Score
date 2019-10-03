![IF FORKED DO NOT REMOVE](etc/flow_diagram.png)

# [A Novel Digital Score for Abundance of Tumour Infiltrating Lymphocytes Predicts Disease Free Survival in Oral Squamous Cell Carcinoma](https://tia-lab.github.io/TILAb-Score/)

### Table of Contents
0. [Introduction](#introduction)
0. [Citation](#citation)
0. [Dataset](#Dataset)
0. [Model](#model)
0. [Prerequisites](#prerequisites)
0. [License](#License)

### Introduction

This repository contains the implementation of TILAb-score as described in the paper.

### Citation

The journal paper on this work has been published in [Nature Scientific Reports](https://www.nature.com/articles/s41598-019-49710-z#Sec17). If you use this code in your research, please cite this work:

	@article{shaban2019novel,
	  title={A novel Digital Score for Abundance of Tumour Infiltrating Lymphocytes predicts Disease free Survival in oral Squamous cell carcinoma},
	  author={Shaban, Muhammad and Khurram, Syed Ali and Fraz, Muhammad Moazam and Alsubaie, Najah and Masood, Iqra and Mushtaq, Sajid and Hassan, Mariam and Loya, Asif and Rajpoot, Nasir M},
	  journal={Scientific reports},
	  volume={9},
	  number={1},
	  pages={1--13},
	  year={2019},
	  publisher={Nature Publishing Group}
	}

### Dataset
The datset for training should be organized in following hierarchy:
```
dataset
   -- train
       -- 0_Stroma
       -- 1_Non_ROI
       -- 2_Tumour
       -- 3_Lymphocyte
   -- valid
       -- 0_Stroma
       -- 1_Non_ROI
       -- 2_Tumour
       -- 3_Lymphocyte
```
Please contact Prof. Nasir Rajpoot (n.m.rajpoot@warwick.ac.uk) for dataset related queries.

### Training
The training.py file in `src/` directory will train the model using the dataset in `dataset/` directory. You may need to tune the hyperparameters for training on your own dataset to train an optimal model.

### Model
The trained model used to produce the results in the paper is available in the `models/` directory.

### Prerequisites
Following software packages will be required to run this code:

```
-- Python 3.5
   -- tensorflow-gpu=1.8.0
   -- keras=2.1.6
   -- openslide
   -- opencv_python
   -- scipy
-- R packages
   -- survival
   -- survMisc
   -- gdata
   -- ggplot2
   -- survminer
   -- rms
```
## Authors

See the list of [contributors](https://github.com/TIA-Lab/TILAb_Score/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](https://github.com/TIA-Lab/TILAb_Score/blob/master/License.md) file for details.
