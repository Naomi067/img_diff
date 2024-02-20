import tensorflow as tf
import numpy as np
from Mydataset import ImageLoader
import glob
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torch.utils.data import DataLoader, Dataset

# class MLP(tf.keras.Model):
#     """自定义MLP类
#     """
#     def __init__(self):
#         super().__init__()
#         # 定义两层神经网络，第一层100个神经元，激活函数relu，第二层10个神经元输出给softmax
#         self.flatten = tf.keras.layers.Flatten()
#         self.dense1 = tf.keras.layers.Dense(units=100, activation=tf.nn.relu)
#         self.dense2 = tf.keras.layers.Dense(units=10)

#     def call(self, inputs):
#         # [batch_size, 28, 28, 1]
#         x = self.flatten(inputs)
#         # [batch_size, 784]
#         x = self.dense1(x)
#         # [batch_size, 100]
#         x = self.dense2(x)
#         # [batch_size, 10]
#         output = tf.nn.softmax(x)
#         return output

# def train(all_imgs_path, batch_size, num_epochs, learning_rate):
#     model = MLP()
#     data_loader = ImageLoader(all_imgs_path, batch_size)
#     optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
#     for epoch in range(num_epochs):
#         for batch_index in range(data_loader.train_num // batch_size):
#             X, y = data_loader.get_train_batch()
#             with tf.GradientTape() as tape:
#                 y_pred = model(X)
#                 loss = tf.keras.losses.sparse_categorical_crossentropy(y_true=y, y_pred=y_pred)
#                 loss = tf.reduce_mean(loss)
#                 print("epoch %d, batch %d: loss %f" % (epoch, batch_index, loss.numpy()))
#             grads = tape.gradient(loss, model.trainable_variables)
#             optimizer.apply_gradients(zip(grads, model.trainable_variables))

class MLP(nn.Module):
    """自定义MLP类
    """
    def __init__(self):
        super(MLP, self).__init__()
        # 定义两层神经网络，第一层100个神经元，激活函数relu，第二层10个神经元输出给softmax
        self.flatten = nn.Flatten()
        self.dense1 = nn.Linear(196608, 256)
        self.dense2 = nn.Linear(256, 3)

    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.dense1(x))
        x = self.dense2(x)
        output = torch.softmax(x, dim=1)
        return output


def train(all_imgs_path, batch_size, num_epochs, learning_rate):
    model = MLP()
    data_loader = ImageLoader(all_imgs_path, batch_size)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    criterion = nn.CrossEntropyLoss()

    for epoch in range(num_epochs):
        for batch_index, (X, y) in enumerate(data_loader.train_dl):
            optimizer.zero_grad()
            y_pred = model(X)
            loss = criterion(y_pred, y)
            print("epoch %d, batch %d: loss %f" % (epoch, batch_index, loss.item()))
            loss.backward()
            optimizer.step()

if __name__ == "__main__":
    data_folder = 'G:/img_diff/tools/trianData/1698894505'
    all_imgs_path = glob.glob(os.path.join(data_folder, '**', '*.jpg'), recursive=True)
    batch_size = 6
    num_epochs = 5
    learning_rate = 0.001
    train(all_imgs_path, batch_size, num_epochs, learning_rate)


















