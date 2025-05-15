###imports###
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import zipfile


# Parameters
DATA_DIR = "C:/Users/mfouc/OneDrive/Desktop/Clash_Cards_Data/" # error here ??
BATCH_SIZE = 32 # depends on cpu/gpu
NUM_EPOCHS = 10 # passes over data
IMG_SIZE = 128
MODEL_PATH = "Models/classifier.pth"

# train model with torch