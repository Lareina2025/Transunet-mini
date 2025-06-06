# Transunet-mini
# 🧠 TransUNet (Mini) - Small-Scale Reproduction for Medical Image Segmentation

This project reproduces the core functionality of the **TransUNet** architecture using only **300 samples** from the Synapse dataset. The goal is to gain a deep understanding of how ViT + CNN hybrids work in medical image segmentation due to compute constraints.

---

## 📌 Project Overview

- **📁 Dataset**: 300 CT slice samples from the [Synapse multi-organ segmentation dataset]
- **🧠 Model**: TransUNet = ResNetV2 + ViT + UNet decoder
- **⚙ Framework**: PyTorch
- **🎯 Task**: Multi-organ segmentation from abdominal CT images

---

## 🔧 My Contributions

- Preprocessed and used 300 small samples to simulate low-resource settings.
- Modified and ran TransUNet training pipeline with limited compute.
- Got segmentation results and assessed model performance.

---

## 🚀 How to Run

### 1. Install dependencies

Please prepare an environment with python=3.7, and then use the command "pip install -r requirements.txt" for the dependencies.

### 2. Prepare data
see sample_selection.md to select 300 samples for training,[The original datasets](https://drive.google.com/file/d/1mYrHyKfOHXcx_YsrLVSSd9gxjsR4OvP2/view?usp=drive_link)
Then rename the training data as train_npz
Download the test data [test_vol_h5](https://drive.google.com/file/d/1_9rmz0gbd1O7VFlCh2cbt3xWr4UEBP_E/view?usp=drive_link) 
You can also just download my samples: [300 samples](https://drive.google.com/file/d/1kAEHmmOzz5A0UN6g4VEzZQWGovjBls8X/view?usp=drive_link)
Put the training data and test data into the folder **data/Synapse**

### 3. download 
Download Google pre-trained ViT models
[Get models in this link](https://console.cloud.google.com/storage/browser/vit_models;tab=objects?pli=1&inv=1&invt=AbzYYg&prefix=&forceOnObjectsSortingFiltering=false): R50-ViT-B_16
### 4. Train the model
python train.py --dataset Synapse --vit_name R50-ViT-B_16

### 5. Test the model
python test.py --dataset Synapse --vit_name R50-ViT-B_16

## 📊 Evaluation Results (12 test cases, 50 epochs, 300 training slices)

| Organ/Class | Dice Score (%) | HD95 (mm) |
|-------------|----------------|-----------|
| Class 1     | 76.09          | 119.57    |
| Class 2     | 60.15          | 72.89     |
| Class 3     | 77.72          | 82.49     |
| Class 4     | 71.44          | 153.87    |
| Class 5     | 87.16          | 80.17     |
| Class 6     | **39.82**      | 21.82     |
| Class 7     | 73.17          | 108.68    |
| Class 8     | 63.98          | 25.97     |

**Overall performance on test set**:

- Mean Dice: **0.6869**
- Mean HD95: **83.18mm**

> ⚠️ Note: Due to limited computational resources, the model was trained with only 300 slices for 50 epochs. Performance is lower than full-dataset training but still provides a baseline reference.


## 🧠 Key Learnings

- Understood how ViT and ResNetV2 cooperate in TransUNet.
- Explored how small datasets affect segmentation generalization.
