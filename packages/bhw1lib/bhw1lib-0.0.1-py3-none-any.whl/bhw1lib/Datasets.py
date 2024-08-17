# Source: https://pytorch.org/tutorials/beginner/basics/data_tutorial.html

import os
import pandas as pd
from torchvision.io import read_image
from torch.utils.data import Dataset


class DatasetFull(Dataset):
    def __init__(self, annotations_file, img_dir, train=True, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
        self.idxs = []

        labels_count = {}
        for idx in range(len(self.img_labels)):
            label = self.img_labels.iloc[idx, 1]
            if label not in labels_count.keys():
                labels_count[label] = 0
            labels_count[label] += 1
            if (train and labels_count[label] % 5 != 0) or (not train and labels_count[label] % 5 == 0):
                self.idxs.append(idx)

    def __len__(self):
        return len(self.idxs)

    def __getitem__(self, idx):
        real_idx = self.idxs[idx]
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[real_idx, 0])
        image = read_image(img_path)
        label = self.img_labels.iloc[real_idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label


class DatasetMedium(Dataset):
    def __init__(self, annotations_file, img_dir, train=True, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
        self.idxs = []

        labels_count = {}
        for idx in range(len(self.img_labels)):
            label = self.img_labels.iloc[idx, 1]
            if label >= 100:
                continue
            if label not in labels_count.keys():
                labels_count[label] = 0
            labels_count[label] += 1
            if (train and labels_count[label] % 5 != 0) or (not train and labels_count[label] % 5 == 0):
                self.idxs.append(idx)

    def __len__(self):
        return len(self.idxs)

    def __getitem__(self, idx):
        real_idx = self.idxs[idx]
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[real_idx, 0])
        image = read_image(img_path)
        label = self.img_labels.iloc[real_idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label


class DatasetSmall(Dataset):
    def __init__(self, annotations_file, img_dir, train=True, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
        self.idxs = []

        labels_count = {}
        for idx in range(len(self.img_labels)):
            label = self.img_labels.iloc[idx, 1]
            if label >= 50:
                continue
            if label not in labels_count.keys():
                labels_count[label] = 0
            labels_count[label] += 1
            if (train and labels_count[label] % 5 != 0) or (not train and labels_count[label] % 5 == 0):
                self.idxs.append(idx)

    def __len__(self):
        return len(self.idxs)

    def __getitem__(self, idx):
        real_idx = self.idxs[idx]
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[real_idx, 0])
        image = read_image(img_path)
        label = self.img_labels.iloc[real_idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label


def get_filename(idx):
    return 'test_' + '0' * (5 - len(str(idx))) + str(idx) + '.jpg'


class DatasetTest(Dataset):
    def save_in_memory(self):
        for i in range(len(self)):
            self.data.append(self[i])

    def __init__(self, img_dir, size, transform=None, save_in_memory=False):
        self.img_dir = img_dir
        self.size = size
        self.transform = transform
        self.data = []
        if save_in_memory:
            self.save_in_memory()

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        if idx < len(self.data):
            return self.data[idx]
        filename = get_filename(idx)
        img_path = os.path.join(self.img_dir, filename)
        image = read_image(img_path)
        if self.transform:
            image = self.transform(image)
        return image
