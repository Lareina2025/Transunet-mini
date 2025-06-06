# Sample Selection Strategy for 300 Training Slices

To construct a compact yet representative training set, we selected **300 axial slices** from the Synapse multi-organ segmentation dataset in a structured manner. The selection process was guided by the following principles:

## 1. Dataset Background

We used the Synapse multi-organ segmentation dataset from the MICCAI 2015 Multi-Atlas Abdomen Labeling Challenge [Link](https://www.synapse.org/#!Synapse:syn3193805/wiki/21778). The dataset contains **30 contrast-enhanced abdominal CT volumes**, totaling **3779 axial slices**. Each CT volume contains **85 to 198 slices**, with image size **512 × 512** and voxel spacing approximately `[0.54 × 0.98 × 2.5 ~ 5.0] mm³`.

## 2. Target Organs

We focus on the **8 abdominal organs** commonly used in previous works:
- Aorta  
- Gallbladder  
- Spleen  
- Left Kidney  
- Right Kidney  
- Liver  
- Pancreas  
- Stomach  

## 3. Filtering Criteria

- **Excluded pure background slices**: Any slice without any labeled organ pixels (i.e., background only) was removed from the candidate pool.  
- **Balanced organ coverage**: For each of the 8 target organs, we computed their occurrence frequency across all labeled slices.  
- **Class-balanced sampling**: We then selected 300 slices such that all organs are **evenly represented** (i.e., the number of slices where each organ appears is as balanced as possible).  
- This ensures the final training subset is **representative** and **organ-balanced**, which is beneficial for training segmentation models under data constraints.

This subset of 300 slices serves as a lightweight version of the full dataset, suitable for experimentation, debugging, or small-scale training with limited computational resources.

> The sample selection script is provided in `select_balanced_samples.py`.
