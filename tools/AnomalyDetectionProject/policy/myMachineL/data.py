import os
import numpy as np
import pandas as pd
import torch
from torchvision import models, transforms
from PIL import Image

# 加载预训练模型
model = models.resnet18(pretrained=True)
model.eval()

# 图片预处理
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 数据集路径和标签
data_dir = 'path/to/your/data'
label_file = 'path/to/your/label/file.csv'

# 获取所有图片路径和标签
image_paths = []
labels = []
for label in os.listdir(data_dir):
    label_dir = os.path.join(data_dir, label)
    for image_name in os.listdir(label_dir):
        image_path = os.path.join(label_dir, image_name)
        image_paths.append(image_path)
        labels.append(label)

# 特征提取和标记
features = []
for image_path in image_paths:
    image = Image.open(image_path)
    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0)
    with torch.no_grad():
        feature_tensor = model(image_tensor)
    feature = feature_tensor.numpy().flatten()
    features.append(feature)

# 标记处理
labels = np.array(labels)
mask = np.random.rand(len(labels)) < 0.1  # 假设有10%的数据是有标记的
labels[mask] = -1  # 有标记的标记为1，无标记的标记为-1
labels[~mask] = np.array([int(l) for l in labels[~mask]])  # 将有标记的标签转为整数类型

# 将特征和标记保存到CSV文件中
data = np.hstack((np.array(features), labels.reshape(-1, 1)))
columns = ['f{}'.format(i) for i in range(data.shape[1] - 1)] + ['label']
df = pd.DataFrame(data=data, columns=columns)
df.to_csv(label_file, index=False)