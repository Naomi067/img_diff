import glob
import torch
from torch.utils import data
from PIL import Image
import numpy as np
from torchvision import transforms
import matplotlib.pyplot as plt
import os
import re

#通过创建data.Dataset子类Mydataset来创建输入
class Mydataset(data.Dataset):
# 类初始化
    def __init__(self, root):
        self.imgs_path = root
# 进行切片
    def __getitem__(self, index):
        img_path = self.imgs_path[index]
        return img_path
# 返回长度
    def __len__(self):
        return len(self.imgs_path)


class Mydatasetpro(data.Dataset):
# 类初始化
    def __init__(self, img_paths, labels, transform):
        self.imgs = img_paths
        self.labels = labels
        self.transforms = transform
# 进行切片
    def __getitem__(self, index):                #根据给出的索引进行切片，并对其进行数据处理转换成Tensor，返回成Tensor
        img = self.imgs[index]
        label = self.labels[index]
        pil_img = Image.open(img)                 #pip install pillow
        data = self.transforms(pil_img)
        return data, label
# 返回长度
    def __len__(self):
        return len(self.imgs)


if __name__ == '__main__':
    data_folder = 'G:/img_diff/tools/TrianData'
    all_imgs_path = glob.glob(os.path.join(data_folder, '**', '*.jpg'), recursive=True)
    print(len(all_imgs_path))
    #利用自定义类Mydataset创建对象fashion_dataset
    fashion_dataset = Mydataset(all_imgs_path)
    # print(len(fashion_dataset)) #返回文件夹中图片总个数
    # print(fashion_dataset[2:5])#切片，显示第12至第十五张图片的路径
    wheather_datalodaer = torch.utils.data.DataLoader(fashion_dataset, batch_size=2) #每次迭代时返回五个数据
    # print(next(iter(wheather_datalodaer)))

    species = ['dress','back','headdress']
    # species_to_id = dict((c, i) for i, c in enumerate(species))
    # # print(species_to_id)
    # id_to_species = dict((v, k) for k, v in species_to_id.items())
    # # print(id_to_species)
    all_labels = []
    #对所有图片路径进行迭代
    for img in all_imgs_path:
        # 使用正则表达式查找路径中匹配的类别名称
        match = re.search(r'\\(dress|back|headdress)\\', img)
        if match:
            # 找到匹配的类别，将其添加到标签列表中
            category = match.group(1)  # 获取匹配的类别名称
            label = species.index(category)  # 获取类别在列表中的索引
            all_labels.append(label)
    print(len(all_labels)) #得到所有标签 

    # 对数据进行转换处理
    transform = transforms.Compose([
                    transforms.Resize((256,256)), #做的第一步转换
                    transforms.ToTensor() #第二步转换，作用：第一转换成Tensor，第二将图片取值范围转换成0-1之间，第三会将channel置前
    ])

    BATCH_SIZE = 10
    fashion_dataset = Mydatasetpro(all_imgs_path, all_labels, transform)
    wheather_datalodaer = data.DataLoader(
                                fashion_dataset,
                                batch_size=BATCH_SIZE,
                                shuffle=True
    )

    imgs_batch, labels_batch = next(iter(wheather_datalodaer))
    print(imgs_batch.shape)

    # plt.figure(figsize=(12, 8))
    # for i, (img, label) in enumerate(zip(imgs_batch[:6], labels_batch[:6])):
    #     img = img.permute(1, 2, 0).numpy()
    #     plt.subplot(2, 3, i+1)
    #     plt.title(id_to_species.get(label.item()))
    #     plt.imshow(img)
    # plt.show()#展示图片
    
    #划分测试集和训练集
    index = np.random.permutation(len(all_imgs_path))

    all_imgs_path = np.array(all_imgs_path)[index]
    all_labels = np.array(all_labels)[index]

    #80% as train
    s = int(len(all_imgs_path)*0.8)
    print(s)

    train_imgs = all_imgs_path[:s]
    train_labels = all_labels[:s]
    test_imgs = all_imgs_path[s:]
    test_labels = all_imgs_path[s:]

    train_ds = Mydatasetpro(train_imgs, train_labels, transform) #TrainSet TensorData
    test_ds = Mydatasetpro(test_imgs, test_labels, transform) #TestSet TensorData
    train_dl = data.DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)#TrainSet Labels
    test_dl = data.DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=True)#TestSet Labels
