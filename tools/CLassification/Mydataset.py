import glob
from typing import Any
import torch
from torch.utils import data
from PIL import Image
import numpy as np
from torchvision import transforms
import matplotlib.pyplot as plt
import os
import re
import cv2
import sys
import random

SPECIES = ['Dress', 'Back', 'Headdress']

def error(message):
    print("[Error]: " + message)
    sys.exit(1)

#通过创建data.Dataset子类Mydataset来创建输入
class ImageDataset(data.Dataset):
    def __init__(self, img_paths, labels, transform):
        self.imgs = img_paths
        self.labels = labels
        self.transforms = transform

    def __getitem__(self, index):
        img_path = self.imgs[index]
        label = self.labels[index]
        cv_img = cv2.imread(img_path)  # 使用cv2读取图像
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)  # 如果需要转换为RGB格式
        cv_img = cv2.resize(cv_img, (256, 256))
        tensor_img = self.transforms(cv_img)  # 应用转换并将图像转换为tensor
        return tensor_img, label

    def __len__(self):
        return len(self.imgs)

def getLabel(all_imgs_path):
    all_labels = []
    #对所有图片路径进行迭代
    for img in all_imgs_path:
        # 使用正则表达式查找路径中匹配的类别名称
        match = re.search(r'(Dress|Back|Headdress)\d+', img, re.I)
        if match:
            # 找到匹配的类别，将其添加到标签列表中
            category = match.group(1)  # 获取匹配的类别名称
            label = SPECIES.index(category)  # 获取类别在列表中的索引
            all_labels.append(label)
    all_labels = torch.tensor(all_labels, dtype=torch.long)
    return all_labels

def getSpecies(label):
    if 0 <= label < len(SPECIES):
        return SPECIES[label]
    else:
        return "Unknown"

def getLabelIndex(species):
    try:
        return SPECIES.index(species)
    except ValueError:
        return -1  # If species is not found, return -1 or handle it as per your requirement

def imgsBatchImshow(imgs_batch, labels_batch):
    # 只展示batch内的6张
    plt.figure(figsize=(12, 8))
    for i, (img, label) in enumerate(zip(imgs_batch[:6], labels_batch[:6])):
        img = img.permute(1, 2, 0).numpy()
        plt.subplot(2, 3, i+1)
        plt.title(getSpecies(label))
        plt.imshow(img)
    plt.show()

class ImageLoader(object):
    def __init__(self, all_imgs_path, batch_size):
        self.all_imgs_path = all_imgs_path
        self.all_labels = getLabel(all_imgs_path)
        self.transform = self._get_transform()
        # self.fashion_dataset = ImageDataset(self.all_imgs_path, self.all_labels, self.transform)
        # self.fashion_dataloder = data.DataLoader(
        #                             self.fashion_dataset,
        #                             batch_size=batch_size,
        #                             shuffle=True
        # )
        self.train_dl, self.test_dl, self.train_num, self.test_num = self._get_train_test_data(batch_size)

    def _get_transform(self):
        return transforms.Compose([
                    transforms.ToTensor()
        ])

    def _get_train_test_data(self,batch_size):
        # 划分测试集和训练集
        index = np.random.permutation(len(self.all_imgs_path))

        self.all_imgs_path = np.array(self.all_imgs_path)[index]
        self.all_labels = np.array(self.all_labels)[index]

        #80% as train
        s = int(len(self.all_imgs_path)*0.8)
        print(s)
        train_num = s
        test_num = len(self.all_imgs_path) - s
        train_imgs = self.all_imgs_path[:s]
        train_labels = self.all_labels[:s]
        test_imgs = self.all_imgs_path[s:]
        test_labels = self.all_labels[s:]

        train_ds = ImageDataset(train_imgs, train_labels, self.transform) #TrainSet TensorData
        test_ds = ImageDataset(test_imgs, test_labels, self.transform) #TestSet TensorData
        train_dl = data.DataLoader(train_ds, batch_size=batch_size, shuffle=True)#TrainSet Labels
        test_dl = data.DataLoader(test_ds, batch_size=batch_size, shuffle=True)#TestSet Labels
        return train_dl, test_dl, train_num, test_num

    # def get_batch(self):
    #     imgs_batch, labels_batch = next(iter(self.fashion_dataloder))
    #     return imgs_batch, labels_batch

    def get_train_batch(self):
        imgs_batch, labels_batch = next(iter(self.test_dl))
        return imgs_batch, labels_batch

    def get_test_batch(self):
        imgs_batch, labels_batch = next(iter(self.test_dl))
        return imgs_batch, labels_batch

if __name__ == '__main__':
    data_folder = 'G:/img_diff/tools/trianData/1698894505'
    # all_imgs_path = glob.glob(os.path.join(data_folder, '**', '*.jpg'), recursive=True)
    # print(len(all_imgs_path))
    # all_labels = getLabel(all_imgs_path)

    # # 定义转换
    # transform = transforms.Compose([
    #                 transforms.ToTensor()
    # ])


    # BATCH_SIZE = 10
    # fashion_dataset = ImageDataset(all_imgs_path, all_labels, transform)
    # fashion_dataloder = data.DataLoader(
    #                             fashion_dataset,
    #                             batch_size=BATCH_SIZE,
    #                             shuffle=True
    # )

    BATCH_SIZE = 10
    all_imgs_path = glob.glob(os.path.join(data_folder, '**', '*.jpg'), recursive=True)
    ImageLoader = ImageLoader(all_imgs_path, BATCH_SIZE)
    
    imgs_batch, labels_batch = ImageLoader.get_train_batch()
    print(imgs_batch.shape)

    # 划分测试集和训练集
    # index = np.random.permutation(len(all_imgs_path))

    # all_imgs_path = np.array(all_imgs_path)[index]
    # all_labels = np.array(all_labels)[index]

    # #80% as train
    # s = int(len(all_imgs_path)*0.8)
    # print(s)

    # train_imgs = all_imgs_path[:s]
    # train_labels = all_labels[:s]
    # test_imgs = all_imgs_path[s:]
    # test_labels = all_imgs_path[s:]

    # train_ds = ImageDataset(train_imgs, train_labels, transform) #TrainSet TensorData
    # test_ds = ImageDataset(test_imgs, test_labels, transform) #TestSet TensorData
    # train_dl = data.DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)#TrainSet Labels
    # test_dl = data.DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=True)#TestSet Labels
